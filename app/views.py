from typing import List, Dict
from urllib.parse import quote
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render

import yandex_music


YANDEX_TOKEN = ""

def main(req: HttpRequest):
    return render(req, "index.html")

def search(req: HttpRequest, text: str = ""):
    if req.method == "POST" and 'search_text' in req.POST:
        q = req.POST.get('search_text', '').strip()
        return HttpResponseRedirect('/' + quote(q) + '/') if q else HttpResponseRedirect('/')

    query = (text or "").strip()
    tracks: List[Dict] = []
    error = None

    if query:
        try:
            client = yandex_music.Client(YANDEX_TOKEN).init()
            try:
                result = client.search(text=query, type_='track')
            except TypeError:
                result = client.search(query)

            if getattr(result, 'tracks', None) and getattr(result.tracks, 'results', None):
                for t in result.tracks.results:
                    artists = ', '.join(a.name for a in t.artists)
                    album = t.albums[0].title if t.albums else ''
                    cover_url = t.get_cover_url(size='200x200') if hasattr(t, 'get_cover_url') else None

                    tracks.append({
                        'title': t.title,
                        'artists': artists,
                        'album': album,
                        'cover_url': cover_url,
                    })

        except Exception as e:
            error = str(e)

    return render(req, "index.html", {'tracks': tracks, 'query': query, 'error': error})
