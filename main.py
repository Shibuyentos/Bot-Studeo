# main.py

import os
from dotenv import load_dotenv
from scraper.studeo_scraper import StudeoScraper

def main():
    load_dotenv()
    cpf = os.getenv("STUDEO_CPF")
    senha = os.getenv("STUDEO_SENHA")
    # MUDANÇA 1: Lemos a variável com o caminho do driver do arquivo .env
    driver_path = os.getenv("EDGE_DRIVER_PATH")

    # MUDANÇA 2: Verificamos se todas as três variáveis existem
    if not all([cpf, senha, driver_path]):
        print("Erro: Verifique se STUDEO_CPF, STUDEO_SENHA e EDGE_DRIVER_PATH estão no arquivo .env")
        return

    # MUDANÇA 3: Passamos o caminho do driver ao criar o scraper
    scraper = StudeoScraper(driver_path=driver_path)
    login_success = scraper.login(cpf, senha)

    if login_success:
        print("\nLogin realizado com sucesso!")
    else:
        print("\nFalha no processo de login.")

    input("Pressione Enter para fechar o navegador...")
    scraper.close()

if __name__ == "__main__":
    main()