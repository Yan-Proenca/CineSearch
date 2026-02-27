from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "af63db86795804321d4287bc6d27fdbe"
BASE_URL = "https://api.themoviedb.org/3"


@app.route("/")
def index():
    page = request.args.get("page", default=1, type=int)
    query = request.args.get("q")
    movie_id = request.args.get("movie_id", type=int)

    filmes = []
    filme = None
    similares = []

# 🎥 DETALHES DO FILME
    if movie_id:
        params = {
            "api_key": API_KEY,
            "language": "pt-BR"
        }

        #Detalhes do filme
        resp_filme = requests.get(
            f"{BASE_URL}/movie/{movie_id}",
            params=params
        )

        if resp_filme.status_code == 200:
            filme = resp_filme.json()
        else:
            filme = None

        #Classificação indicativa (Brasil)
        classificacao = "Livre"
        resp_age = requests.get(
            f"{BASE_URL}/movie/{movie_id}/release_dates",
            params={"api_key": API_KEY}
        )

        if resp_age.status_code == 200:
            age_data = resp_age.json()
            for country in age_data.get("results", []):
                if country.get("iso_3166_1") == "BR":
                    if country.get("release_dates"):
                        cert = country["release_dates"][0].get("certification")
                        if cert:
                            classificacao = cert
                    break

        if filme:
            filme["classificacao"] = classificacao

        #Filmes similares
        resp_similares = requests.get(
            f"{BASE_URL}/movie/{movie_id}/similar",
            params=params
        )

        if resp_similares.status_code == 200:
            similares = resp_similares.json().get("results", [])
            # Remove filmes sem poster
            similares = [s for s in similares if s.get("poster_path")]
        else:
            similares = []


#BUSCA DE FILMES
    elif query:
        params = {
            "api_key": API_KEY,
            "language": "pt-BR",
            "query": query,
            "page": page
        }

        resp_busca = requests.get(
            f"{BASE_URL}/search/movie",
            params=params
        )

        if resp_busca.status_code == 200:
            filmes = resp_busca.json().get("results", [])
            filmes = [f for f in filmes if f.get("poster_path")]
        else:
            filmes = []

#FILMES POPULARES
    else:
        params = {
            "api_key": API_KEY,
            "language": "pt-BR",
            "page": page
        }

        resp_popular = requests.get(
            f"{BASE_URL}/movie/popular",
            params=params
        )

        if resp_popular.status_code == 200:
            filmes = resp_popular.json().get("results", [])
            filmes = [f for f in filmes if f.get("poster_path")]
        else:
            filmes = []

# ENVIO PARA O HTML
    return render_template(
        "index.html",
        filmes=filmes,
        filme=filme,
        similares=similares,
        page=page,
        query=query
    )
if __name__ == "__main__":
    app.run(debug=True)