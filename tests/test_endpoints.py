def test_criar_time(client):
    """
    Testa a criação de um novo time com sucesso.
    """
    response = client.post(
        "/times/",
        json={"nome": "Unidos do Teste FC", "estadio": "Estádio da Memória", "presidente": "Pytest"},
    )
    data = response.json()
    assert response.status_code == 200
    assert data["nome"] == "Unidos do Teste FC"
    assert "id" in data


def test_sorteio_bloqueado_se_ja_existir_partida(client):
    """
    Testa a regra de negócio que impede um novo sorteio se já houver partidas.
    """
    client.post("/times/", json={"nome": "Time A", "estadio": "A", "presidente": "A"})
    client.post("/times/", json={"nome": "Time B", "estadio": "B", "presidente": "B"})

    primeiro_sorteio = client.post("/sorteio/")
    assert primeiro_sorteio.status_code == 200
    assert len(primeiro_sorteio.json()) == 1

    segundo_sorteio = client.post("/sorteio/")
    assert segundo_sorteio.status_code == 400
    assert "Um sorteio já foi realizado" in segundo_sorteio.json()["detail"]


def test_listar_partidas_vazias(client):
    """
    Testa se a lista de partidas está vazia antes do sorteio.
    """
    response = client.get("/partidas/")
    assert response.status_code == 200
    assert response.json() == []


def test_listar_partidas_apos_sorteio(client):
    """
    Testa se a lista de partidas é retornada corretamente após o sorteio.
    """
    client.post("/times/", json={"nome": "Time C", "estadio": "C", "presidente": "C"})
    client.post("/times/", json={"nome": "Time D", "estadio": "D", "presidente": "D"})
    client.post("/sorteio/")

    response = client.get("/partidas/")
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["time1"]["nome"] in ["Time C", "Time D"]
    assert data[0]["time2"]["nome"] in ["Time C", "Time D"]
