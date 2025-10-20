# main.py

import os
from dotenv import load_dotenv
from scraper.studeo_scraper import StudeoScraper

def main():
    load_dotenv()
    cpf = os.getenv("STUDEO_CPF")
    senha = os.getenv("STUDEO_SENHA")
    driver_path = os.getenv("EDGE_DRIVER_PATH")

    if not all([cpf, senha, driver_path]):
        print("Erro: Verifique se STUDEO_CPF, STUDEO_SENHA e EDGE_DRIVER_PATH estão no arquivo .env")
        return

    scraper = StudeoScraper(driver_path=driver_path)
    login_success = scraper.login(cpf, senha)

    if login_success:
        print("\nLogin realizado com sucesso!")
        
        atividades_pendentes = scraper.checar_atividades_pendentes()
        
        atividades_com_prazo = [atv for atv in atividades_pendentes if atv["prazo"] != "N/A"]

        if atividades_com_prazo:
            print("\n--- ATIVIDADES PENDENTES ENCONTRADAS ---")
            for atividade in atividades_com_prazo:
                print(f"  Disciplina: {atividade['disciplina']}")
                print(f"  Status: {atividade['status']}")
                print(f"  Prazo: {atividade['prazo']}")
                print("  ---------------------------------")
        else:
            print("\nÓtima notícia! Nenhuma atividade pendente encontrada.")

    else:
        print("\nFalha no processo de login.")

    input("\nPressione Enter para fechar o navegador...")
    scraper.close()

if __name__ == "__main__":
    main()