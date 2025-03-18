from http.server import SimpleHTTPRequestHandler, HTTPServer
import urllib.parse
import os
from db import get_anime_list, get_anime_by_id, init_db

PORT = 8080
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WWW_DIR = os.path.join(BASE_DIR, '../www')

class AnimeHandler(SimpleHTTPRequestHandler):

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)

        # Serve the homepage
        if parsed_path.path == '/':
            self.serve_file('index.html')

        # Serve anime list
        elif parsed_path.path == '/genres':
            animes = get_anime_list()
            anime_html = ''.join(
                f'''
                <div>
                    <a href="/anime/{anime[0]}">
                        <img src="{anime[3]}" alt="{anime[1]}" width="200">
                        <h3>{anime[1]}</h3>
                        <p>Genre: {anime[2]}</p>
                    </a>
                </div>
                ''' for anime in animes
            )
            self.render_template('genres.html', content=anime_html)

        # Serve anime detail
        elif parsed_path.path.startswith('/anime/'):
            anime_id = parsed_path.path.split('/')[-1]
            anime = get_anime_by_id(anime_id)

            if anime:
                self.render_template('player.html', 
                    title=anime[1],
                    description=anime[2],
                    genre=anime[3],
                    release_date=anime[4],
                    image=anime[5],
                    video_url=anime[6]
                )
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"Anime not found")

        # Serve static files
        elif parsed_path.path.startswith('/assets/'):
            self.serve_file(parsed_path.path[1:])
        
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Page not found")

    def serve_file(self, filepath):
        """Serve static files"""
        full_path = os.path.join(WWW_DIR, filepath)
        
        if os.path.exists(full_path):
            self.send_response(200)
            if filepath.endswith('.html'):
                self.send_header('Content-type', 'text/html')
            elif filepath.endswith('.css'):
                self.send_header('Content-type', 'text/css')
            elif filepath.endswith('.js'):
                self.send_header('Content-type', 'application/javascript')
            self.end_headers()

            with open(full_path, 'rb') as file:
                self.wfile.write(file.read())
        else:
            self.send_response(404)
            self.end_headers()

    def render_template(self, template_name, **kwargs):
        """Render HTML template with placeholders"""
        template_path = os.path.join(WWW_DIR, template_name)

        if os.path.exists(template_path):
            with open(template_path, 'r') as file:
                html = file.read().format(**kwargs)
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

def run():
    init_db()
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, AnimeHandler)
    print(f"Server running on port {PORT}")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
