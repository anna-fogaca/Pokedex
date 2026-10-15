import requests
import ipywidgets as widgets
from IPython.display import display, Image, clear_output, HTML


campo = widgets.Text (
    placeholder = 'digite o nome do Pokémon',
    description = 'Pokémon'
)

botao = widgets.Button(
    description = 'buscar',
    button_style = 'success'
)

botao_tipo = widgets.Button(
    description = 'buscar pelo tipo',
     button_style = 'info' ,
    icon = 'filter'
)

saida = widgets.Output()

def buscar_pokemon(b):
  with saida:
    clear_output()
    pokemon = campo.value.lower()
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon}"
    resposta = requests.get(url)
    stats = []
    if resposta.status_code == 200:
      dados = resposta.json()
      nome = dados ["name"].title()
      altura = dados ["height"] / 10
      peso = dados["weight"] / 10

      for stat in dados["stats"]:
        nome_stat = stat["stat"]["name"]
        valor = stat["base_stat"]
        stats.append(f"<li><b>{nome_stat.title()}:</b> {valor}</li>")

      tipos = []
      for tipo in dados ["types"]:
        tipos.append(tipo["type"]["name"])
      imagem = dados["sprites"]["front_default"]
      display(HTML(f"""
      <div style="
            text-align: center;
            font-size: 24px;
            font-family: Arial;
        ">
            <h1>{nome}</h1>
            <p><b>Altura:</b> {altura} m</p>
            <p><b>Peso:</b> {peso} kg</p>
            <p><b>Tipos: </b> {','.join(tipo.title() for tipo in
            tipos)}</p>

            <h3> Status Base </h3>
            <ul style="list-style: none; padding: 0;">
              {''.join(stats)}
            </ul>
          </div>
          """))
      display(HTML(f"""
        <div style="text-align: center;">
          <img src="{imagem}" width="250">
          </div>
          """))

    else:
       display(HTML("""
       <h2 style='color: red; text-align=center;'>
       Pokémon não encontrado!
       </h2>
       """))

def buscar_por_tipo(b):
  with saida:
    clear_output()
    tipo = campo.value.strip().lower()
    if not tipo:
      display(HTML("<p style='color: orange;'>digite um tipo de Pokémon</p>"))
      return

    url = f"https://pokeapi.co/api/v2/type/{tipo}"

    try:
        resposta = requests.get(url, timeout=5)
        resposta.raise_for_status()
        dados = resposta.json()
        for p in dados["pokemon"][:15]:
          pokemon_html = ""
          nome = p["pokemon"]["name"].title()
          # extrai o ID do Pokémon pela PokeApi
          url_pokemon = p["pokemon"]["url"]
          pokemon_id = url_pokemon.rstrip("/").split("/")[-1]

          imagem = (
              f"https://raw.githubusercontent.com/"
              f"PokeAPI/sprites/master/sprites/pokemon/{pokemon_id}.png"
          )
          pokemon_html += f"""
          <div style="
            display: flex;
            align-items: center;
            margin: 10px 0;
            font-size: 18px;
          ">
          <img src="{imagem}" width="70">
          <span style="margin-left: 15px;">
            {nome}
          </span>
          </div>
          """
          display(HTML(f"""
          <div style="
              font-family: Arial;
              max-width: 400px;
              margin: auto;
          ">
          <h2 style="text=align: center;">
              Pokémon do tipo {tipo.title()}
          </h2>
          {pokemon_html}
          </div>
          """))


    except requests.exceptions.RequestException:
       display(HTML("<h3 style='color:red;'> Erro ao acessar a API</h3>"))
    except KeyError:
      display(HTML("<h3 style='color:red;'> tipo inválido!</h3>"))


botao.on_click(buscar_pokemon)
display(campo)
display(botao)
display(saida)
display(botao_tipo)
botao_tipo.on_click(buscar_por_tipo)
