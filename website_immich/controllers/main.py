import logging
import mimetypes
import requests
import werkzeug.exceptions

from odoo import http, tools, _
from odoo.http import request
from odoo.tools.mimetypes import guess_mimetype

from odoo.addons.html_editor.controllers.main import HTML_Editor

logger = logging.getLogger(__name__)


class Web_Immich(http.Controller):

    def _get_immich_config(self):
        ICP = request.env['ir.config_parameter'].sudo()
        return {
            'url': ICP.get_param('immich.url', '').rstrip('/'),
            'api_key': ICP.get_param('immich.api_key', ''),
        }

    def _immich_headers(self):
        config = self._get_immich_config()
        return {
            'x-api-key': config['api_key'],
            'Accept': 'application/json',
        }

    def _immich_url(self, path):
        config = self._get_immich_config()
        return f"{config['url']}/api{path}"

    def _asset_to_dict(self, item, config):
        """Convert an Immich asset item to our image dict format."""
        if item.get('type') != 'IMAGE':
            return None
        return {
            'id': item['id'],
            'type': 'IMAGE',
            'url': f"/website_immich/thumbnail/{item['id']}",
            'original_url': f"{config['url']}/api/assets/{item['id']}/original",
            'original_filename': item.get('originalFileName', ''),
            'thumbhash': item.get('thumbhash', ''),
            'exif_info': {
                'width': item.get('exifInfo', {}).get('exifImageWidth'),
                'height': item.get('exifInfo', {}).get('exifImageHeight'),
            },
        }

    def _search_people(self, query, config):
        """Search for people matching the query. Returns list of person dicts."""
        try:
            resp = requests.get(
                self._immich_url('/people'),
                headers=self._immich_headers(),
                params={'page': 1, 'size': 100},
                timeout=15,
            )
            if resp.status_code == 200:
                people = resp.json()
                items = people if isinstance(people, list) else people.get('people', people.get('data', []))
                matches = [p for p in items if query.lower() in (p.get('name', '') or '').lower()]
                return matches[:5]
        except requests.exceptions.RequestException:
            logger.debug("People search failed, trying alternative endpoint")
        try:
            resp = requests.get(
                self._immich_url('/search/person'),
                headers=self._immich_headers(),
                params={'name': query},
                timeout=15,
            )
            if resp.status_code == 200:
                data = resp.json()
                return data if isinstance(data, list) else [data]
        except requests.exceptions.RequestException:
            logger.debug("Search-person endpoint not available")
        return []

    def _get_person_assets(self, person_id, page, size, config):
        """Get assets for a specific person."""
        for endpoint in [f'/people/{person_id}/assets', f'/person/{person_id}/assets']:
            try:
                resp = requests.get(
                    self._immich_url(endpoint),
                    headers=self._immich_headers(),
                    params={'page': page, 'size': size},
                    timeout=30,
                )
                if resp.status_code == 200:
                    data = resp.json()
                    items = data if isinstance(data, list) else data.get('items', data.get('data', []))
                    images = [self._asset_to_dict(item, config) for item in items if item.get('type') == 'IMAGE']
                    images = [img for img in images if img]
                    total = data.get('total', len(images)) if not isinstance(data, list) else len(images)
                    return images, total
            except requests.exceptions.RequestException:
                continue
        return [], 0

    def _search_smart(self, query, page, size, config):
        """Search Immich by CLIP smart search (understands image content/context).
        Requires immich-machine-learning service to be running."""
        try:
            response = requests.post(
                self._immich_url('/search/smart'),
                headers=self._immich_headers(),
                json={'query': query, 'page': page, 'size': size},
                timeout=30,
            )
            if response.status_code == 200:
                data = response.json()
                items = data.get('items', data.get('assets', {}).get('items', []))
                total = data.get('total', data.get('assets', {}).get('total', len(items)))
                images = [self._asset_to_dict(item, config) for item in items]
                images = [img for img in images if img]
                return images, total
            elif response.status_code == 501:
                logger.info("Smart search not available (ML service not running)")
        except requests.exceptions.RequestException:
            pass
        return [], 0

    def _search_metadata(self, query, page, size, config):
        """Search Immich by metadata (covers location, filename, description)."""
        try:
            response = requests.post(
                self._immich_url('/search/metadata'),
                headers=self._immich_headers(),
                json={'query': query, 'page': page, 'size': size},
                timeout=30,
            )
            if response.status_code == 200:
                data = response.json()
                assets = data.get('assets', {})
                items = assets.get('items', [])
                total = assets.get('total', 0)
                images = [self._asset_to_dict(item, config) for item in items]
                images = [img for img in images if img]
                return images, total
        except requests.exceptions.RequestException:
            pass
        return [], 0

    @http.route('/website_immich/fetch_images', type='json', auth='user')
    def fetch_immich_images(self, **post):
        config = self._get_immich_config()
        if not config['url'] or not config['api_key']:
            if not request.env.user._can_manage_immich_settings():
                return {'error': 'no_access'}
            return {'error': 'config_not_found'}

        query = post.get('query', '').strip()
        page = post.get('page', 1)
        size = post.get('size', 30)
        search_type = post.get('search_type', 'auto')

        try:
            images = []
            total = 0

            if search_type == 'auto' and query:
                people = self._search_people(query, config)
                if people:
                    logger.info("Person search for '%s' matched: %s", query, [p.get('name') for p in people])
                    person = people[0]
                    images, total = self._get_person_assets(person['id'], page, size, config)
                    if not images:
                        images, total = self._search_metadata(query, page, size, config)
                else:
                    images, total = self._search_smart(query, page, size, config)
                    if not images:
                        images, total = self._search_metadata(query, page, size, config)
            else:
                images, total = self._search_metadata(query, page, size, config)

            return {
                'images': images,
                'total': total,
                'page': page,
            }
        except requests.exceptions.ConnectionError:
            return {'error': 'connection_error'}
        except requests.exceptions.Timeout:
            return {'error': 'timeout'}
        except Exception as e:
            logger.exception("Immich search failed: %s", e)
            return {'error': 'unknown'}

    @http.route('/website_immich/attachment/add', type='json', auth='user', methods=['POST'])
    def save_immich_asset(self, assets=None, **kwargs):
        if not assets:
            return []

        uploads = []
        query = kwargs.get('query', '')
        query = "".join([c for c in query if c.isalnum() or c in list("- ")])[:128]

        res_model = kwargs.get('res_model', 'ir.ui.view')
        if res_model != 'ir.ui.view' and kwargs.get('res_id'):
            res_id = int(kwargs['res_id'])
        else:
            res_id = None

        config = self._get_immich_config()

        for asset_id, value in assets.items():
            original_url = value.get('original_url')
            if not original_url:
                continue
            try:
                headers = self._immich_headers()
                headers['Accept'] = '*/*'
                req = requests.get(original_url, headers=headers, timeout=60)
                if req.status_code != requests.codes.ok:
                    continue
                image = req.content
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
                logger.exception("Failed to download asset %s: %s", asset_id, e)
                continue

            image = tools.image_process(image, verify_resolution=True)
            mimetype = guess_mimetype(image)
            ext = mimetypes.guess_extension(mimetype) or ''

            url_frags = ['immich', asset_id, query + ext]

            attachment_data = {
                'name': '_'.join(url_frags),
                'url': '/' + '/'.join(url_frags),
                'data': image,
                'res_id': res_id,
                'res_model': res_model,
            }
            attachment = HTML_Editor._attachment_create(self, **attachment_data)
            if value.get('description'):
                attachment.description = value.get('description')
            attachment.generate_access_token()
            uploads.append(attachment._get_media_info())

        return uploads

    @http.route('/website_immich/save_config', type='json', auth='user')
    def save_config(self, **post):
        if request.env.user._can_manage_immich_settings():
            request.env['ir.config_parameter'].sudo().set_param(
                'immich.url', post.get('url', '').rstrip('/'))
            request.env['ir.config_parameter'].sudo().set_param(
                'immich.api_key', post.get('api_key', ''))
            return True
        raise werkzeug.exceptions.NotFound()

    @http.route('/website_immich/test_connection', type='json', auth='user')
    def test_connection(self, **post):
        try:
            config = self._get_immich_config()
            url = post.get('url', config['url']).rstrip('/')
            api_key = post.get('api_key', config['api_key'])
            headers = {'x-api-key': api_key, 'Accept': 'application/json'}
            resp = requests.get(
                f"{url}/api/server/about",
                headers=headers,
                timeout=15,
            )
            if resp.status_code == 200:
                return {'success': True}
            elif resp.status_code == 401:
                return {'success': False, 'error': 'unauthorized'}
            else:
                return {'success': False, 'error': str(resp.status_code)}
        except requests.exceptions.ConnectionError:
            return {'success': False, 'error': 'connection_error'}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    @http.route('/website_immich/thumbnail/<asset_id>', type='http', auth='user')
    def proxy_thumbnail(self, asset_id, size='preview'):
        config = self._get_immich_config()
        if not config['url'] or not config['api_key']:
            raise werkzeug.exceptions.NotFound()

        url = f"{config['url']}/api/assets/{asset_id}/thumbnail?size={size}"
        headers = self._immich_headers()
        headers['Accept'] = '*/*'

        try:
            resp = requests.get(url, headers=headers, timeout=30)
            if resp.status_code != 200:
                logger.warning("Immich thumbnail proxy failed for %s: %s", asset_id, resp.status_code)
                raise werkzeug.exceptions.NotFound()
            return request.make_response(resp.content, [
                ('Content-Type', resp.headers.get('Content-Type', 'image/jpeg')),
                ('Cache-Control', 'public, max-age=3600'),
            ])
        except requests.exceptions.RequestException as e:
            logger.exception("Immich thumbnail proxy error for %s: %s", asset_id, e)
            raise werkzeug.exceptions.NotFound()
