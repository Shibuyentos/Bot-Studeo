# Endpoints extraídos (deduplicados e saneados)

> Normalização: IDs → `{id}`, UUID → `{uuid}`, hashes → `{hash}`, tokens/JWT → `{token}`. Query mantém só chaves.

> Total de endpoints únicos: **46**

- **POST** `https://studeoapi.unicesumar.edu.br/log-acesso-api-controller/api/evento/`  _(calls: 21, status: 200:21)_
  - Request: `{"idSessao": {"id": 866574440}, "idTipoEvento": {"dsTipoEvento": "LOGIN"}, "idTipoConteudo": {"dsTipoConteudo": "LOGIN"}, "cdUsuario": "25023123-2", "cdCurso": "PGO_CST_ADSIS", "cdShortname": null, "c...`
  - Response: `{"id": 10008287024, "idSessao": {"id": 866605521, "idFormaAcesso": null, "cdUsuario": null, "dsDispositivoAcesso": null, "dsBrowser": null, "vlLatitude": null, "vlLongitude": null, "token": null}, "id...`
- **GET** `https://studeoapi.unicesumar.edu.br/auth-api-controller/auth/token/time-info`  _(calls: 17, status: 200:17)_
  - Response: `{"datetime": "2026-02-26T20:55:21.841-0300", "offset": -180, "timezone": "-0300", "timezoneId": "America/Sao_Paulo", "timestamp": 1772150121841}`
- **GET** `https://studeoapi.unicesumar.edu.br/atendimento-api-controller/api/atendimento/push`  _(calls: 13, status: 200:13)_
  - Response: `{"list": [{"idConversa": 5012280, "qtaMsg": 1, "aviso": true, "finalizada": false, "solicitaFinalizar": false, "mensagem": null}, {"idConversa": 5012313, "qtaMsg": 1, "aviso": true, "finalizada": fals...`
- **GET** `https://studeoapi.unicesumar.edu.br/ambiente-api-controller/api/aluno/disciplina/curricular/false`  _(calls: 8, status: 200:8)_
  - Response: `[{"tpMatricula": "MATRICULADO", "tpDetalhe": "Nao curricular", "idDisciplina": 312376, "nmDisciplina": "GIRO EAD", "cdShortname": "MDL_AC_7158", "flAtivo": true, "dhLiberar": null, "ano": 2026, "semes...`
- **GET** `https://studeoapi.unicesumar.edu.br/auth-api-controller/api/rota-app/autorizacao`  _(calls: 6, status: 200:6)_
  - Response: `{"access.login": true, "app.nest.aluno.ambiente.negocia-dividas.index": true, "app.nest.aluno.ambiente.acomp-curso.list": true, "app.nest.admin.cpa.tag": true, "app.forms.elements": true, "app.nest.al...`
- **GET** `https://studeoapi.unicesumar.edu.br/auth-api-controller/api/parametro/autorizacao`  _(calls: 6, status: 0:1, 200:5)_
  - Response: `{"PARAM_FORUM_NOTA_MAX": "40", "PARAM_SISTEMA_RUBINHO": "700", "PARAM_PERIODO_CONSULTA_PLANO_ESTUDO_GERAL": "7", "PARAM_PAGINA_INICIAL_TEMPLATE_NAME": "template-aluno", "QUESTIONARIO_VERIFICA_INADIMPL...`
- **GET** `https://api-financial.vitru.com.br/api/rest/billing/method/renegotiation/{id}/LY_PGO_CST_ADSIS`  _(calls: 6, status: 0:1, 200:5)_
  - Response: `{"type": "OLD"}`
- **GET** `https://studeoapi.unicesumar.edu.br/controle-acesso-api-controller/api/usuario-foto/{id}`  _(calls: 6, status: 200:2, 204:4)_
  - Response: `{"idUsuarioFoto": 20803240, "cdUsuario": "25050325-5", "idCentralAnexo": 20803240}`
- **GET** `https://studeoapi.unicesumar.edu.br/atendimento-api-controller/api/atendimento/push?init`  _(calls: 6, status: 200:6)_
  - Response: `{"list": [{"idConversa": 5012280, "qtaMsg": 1, "aviso": true, "finalizada": false, "solicitaFinalizar": false, "mensagem": null}, {"idConversa": 5012313, "qtaMsg": 1, "aviso": true, "finalizada": fals...`
- **POST** `https://studeoapi.unicesumar.edu.br/auth-api-controller/auth/token/create`  _(calls: 4, status: 200:4)_
  - Request: `{"username": "80070107939", "password": "Renann1."}`
- **GET** `https://studeoapi.unicesumar.edu.br/auth-api-controller/api/permissao/autorizacao`  _(calls: 4, status: 200:4)_
  - Response: `{"MENU_LATERAL_ALUNO_SERVICOS_ATUALIZAR_DADOS_CADASTRAIS": true, "MENU_LATERAL_ALUNO_DIPLOMA_DIGITAL": true, "MENU_LATERAL_CERTIFICADO_ALUNOS_CONCLUIDOS": true, "MENU_LATERAL_ALUNO_BIBLIOTECAS_BIBLIOT...`
- **GET** `https://studeoapi.unicesumar.edu.br/controle-acesso-api-controller/api/usuario-regra/existe-regra`  _(calls: 4, status: 200:2, 204:2)_
- **GET** `https://studeoapi.unicesumar.edu.br/controle-acesso-api-controller/api/usuario/info-login`  _(calls: 4, status: 200:4)_
  - Response: `{"id": 2494641, "cdUsuario": "25050325-5", "nmUsuario": "Kauann Gabriel Shibuya", "dsEmail": "RA250503255@EAD.CESUMAR.BR", "dhUltimoAcesso": 1772150120322, "nmPerfil": "ALUNO", "curso": null, "modalid...`
- **POST** `https://studeoapi.unicesumar.edu.br/log-acesso-api-controller/api/sessao/`  _(calls: 4, status: 200:4)_
  - Request: `{"cdUsuario": "25023123-2", "idFormaAcesso": {"dsFormaAcesso": "WEB"}, "dsBrowser": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)", "vlLatitude": null, "vlLongitude...`
  - Response: `{"id": 866605521, "idFormaAcesso": {"id": 2, "dsFormaAcesso": "WEB"}, "cdUsuario": "25050325-5", "dsDispositivoAcesso": null, "dsBrowser": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...`
- **POST** `https://studeoapi.unicesumar.edu.br/log-acesso-api-controller/api/navegador-detalhe/`  _(calls: 4, status: 200:4)_
  - Request: `{"idSessao": {"id": 866574440}, "dsBrowser": "Google Chrome or Chromium", "dsIPAddress": "0.0.0.0"}`
  - Response: `{"id": 677521526, "idNavegadorDetalhe": 677521526, "idSessao": {"id": 866605521, "idFormaAcesso": null, "cdUsuario": null, "dsDispositivoAcesso": null, "dsBrowser": null, "vlLatitude": null, "vlLongit...`
- **GET** `https://studeoapi.unicesumar.edu.br/ambiente-api-controller/api/internet-patrocinada/validar-acesso`  _(calls: 4, status: 200:4)_
  - Response: `{"flInternet": true, "dsMensagem": "Ola aluno! Sua internet patrocinada está ativa."}`
- **GET** `https://studeoapi.unicesumar.edu.br/lyceum-api-controller/api/portal-parceiro/grupo`  _(calls: 4, status: 200:4)_
  - Response: `["0"]`
- **GET** `https://studeoapi.unicesumar.edu.br/ambiente-api-controller/api/aluno/disciplina/active`  _(calls: 4, status: 200:4)_
  - Response: `["1"]`
- **GET** `https://studeoapi.unicesumar.edu.br/ambiente-api-controller/api/controle-servico/ativa/BANNER/WEB`  _(calls: 4, status: 200:4)_
  - Response: `{"responseStatus": "OK", "responseMessage": null, "entity": true}`
- **GET** `https://studeoapi.unicesumar.edu.br/ambiente-api-controller/api/aluno/disciplina/curricular/true`  _(calls: 4, status: 200:4)_
  - Response: `[{"tpMatricula": "Matriculado", "tpDetalhe": "Curricular", "idDisciplina": 766981, "nmDisciplina": "ANÁLISE E PROJETO ORIENTADO A OBJETOS", "cdShortname": "2026_26_EGRAD_ADSIS5E-51_EGRAD_GRAD_080_0026...`
- **GET** `https://studeoapi.unicesumar.edu.br/ambiente-api-controller/api/banner/active/homeBannerDisciplinas`  _(calls: 4, status: 200:4)_
  - Response: `[{"dhInsert": 1748867488183, "dhUpdate": 1751457679523, "dsBanner": "PREPARE-SE", "dhInicio": 1748746800000, "dhFim": 1782874740000, "dsImagemWeb": "acc87654af83d997499bb549c8aaeafef7ee29a0714ad9a767f...`
- **GET** `https://studeoapi.unicesumar.edu.br/ambiente-api-controller/api/banner/search/active`  _(calls: 4, status: 200:4)_
  - Response: `[{"idBanner": 1510, "dsBanner": "Alteração de CNPJ - GRAD. EAD", "dsImagemWeb": "918cf4a8ff0f2b3d947047759fe0de4413bb235c6c678ac4d7c83e807a0c48bad1a67377f76c5c4d0d5578a37e9646e3a7141da07b33ea890311a59...`
- **GET** `https://studeoapi.unicesumar.edu.br/iam-api-controller/api/usuario/quantidade-usuarios`  _(calls: 4, status: 200:4)_
  - Response: `{"cpf": "80070107939", "qtdUsuario": "2"}`
- **GET** `https://studeoapi.unicesumar.edu.br/objeto-ensino-api-controller/api/plano-estudo/disciplinas-usuario`  _(calls: 4, status: 200:2, 204:2)_
  - Response: `[{"dhInicial": 1771930800000, "dhFinal": 1771988340000, "dsPlanoDeEstudoTipoEvento": "Aula", "dsPlanoDeEstudoSubTipoEvento": "AULA", "dsPlanoDeEstudoTipoAlerta": "Aula", "tpCor": "success", "nmDiscipl...`
- **GET** `https://studeoapi.unicesumar.edu.br/ambiente-api-controller/api/aluno/disciplina/afazer`  _(calls: 4, status: 200:4)_
  - Response: `{"somaTotal": 70}`
- **GET** `https://studeo.unicesumar.edu.br/`  _(calls: 3, status: 200:3)_
  - Response: `<!DOCTYPE html> <html lang="pt-BR" data-ng-app="app" ng-strict-di ng-controller="AppCtrl"> <head> <meta http-equiv="content-type" content="text/html;charset=UTF-8"/> <meta charset="utf-8"/> <title ncy...`
- **GET** `https://studeo.unicesumar.edu.br/{token}`  _(calls: 3, status: 200:3)_
  - Response: `{"short_name": "Studeo", "name": "STUDEO - SEU AMBIENTE VIRTUAL DE APRENDIZAGEM", "icons": [{"src": "br/edu/unicesumar/web-angular-layout/src/pages/ico/s-48.0460f2e9.png", "type": "image/png", "sizes"...`
- **GET** `https://studeoapi.unicesumar.edu.br/lyceum-api-controller/api/servicos/dados-cadastrais`  _(calls: 2, status: 200:2)_
- **GET** `https://studeoapi.unicesumar.edu.br/controle-acesso-api-controller/api/usuario/usuarios/{id}`  _(calls: 2, status: 200:2)_
- **POST** `https://api-areasegura.vitru.com.br/security/check`  _(calls: 2, status: 200:2)_
  - Request: `{"username": "80070107939", "birthDay": "05/05/2007"}`
- **GET** `https://studeoapi.unicesumar.edu.br/lyceum-api-controller/api/vem-comigo/permissao`  _(calls: 2, status: 204:2)_
- **POST** `https://studeoapi.unicesumar.edu.br/auth-api-controller/auth/token/renew`  _(calls: 2, status: 200:2)_
  - Request: `{"refreshToken": "eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIyNTA1MDMyNS01IiwiZGF0Ijp7InJ1dCI6bnVsbCwiZGVmIjp7Ik5FU1QiOiJBTFVOTyJ9LCJ0cnMiOmZhbHNlLCJlbWwiOiJSQTI1MDUwMzI1NUBFQUQuQ0VTVU1BUi5CUiIsIml0ZyI6dHJ1ZSwic...`
  - Response: `{"token": "eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIyNTA1MDMyNS01IiwiZGF0Ijp7InJ1dCI6bnVsbCwiZGVmIjp7Ik5FU1QiOiJBTFVOTyJ9LCJ0cnMiOmZhbHNlLCJlbWwiOiJSQTI1MDUwMzI1NUBFQUQuQ0VTVU1BUi5CUiIsIml0ZyI6dHJ1ZSwicm9sIjp7...`
- **GET** `https://studeoapi.unicesumar.edu.br/controle-acesso-api-controller/api/usuario-regra`  _(calls: 2, status: 200:2)_
  - Response: `[{"id": 91798479, "idUsuarioRegra": 91798479, "usuario": {"id": 2494641, "nmUsuario": "Kauann Gabriel Shibuya", "cdUsuario": "25050325-5", "dhInsert": 1732349560695, "dhUpdate": 1764569372981}, "regra...`
- **GET** `https://studeoapi.unicesumar.edu.br/lyceum-api-controller/api/servico-dp-especial/`  _(calls: 2, status: 200:2)_
  - Response: `[]`
- **GET** `https://studeoapi.unicesumar.edu.br/central-anexo-api-controller/api/anexo/findBy/{id}`  _(calls: 2, status: 200:2)_
  - Response: `{"id": 20803240, "nmOriginalArquivo": "IMG_2057.jpg", "dsPath": "arquivo-geral", "cdHash": "f869cf0d69209ad57ae9d433d6a4c8e5cdf423aad34e5aa2bfc2541680f6c90847fdf124fdf592921f3b09faef622914802a31068d4d...`
- **GET** `https://conteudoava.unicesumar.edu.br/display/arquivo-banner-web/6f1842cd8abb5bab69fa64f49503631b022bf2a26777c4f3a00eb5557ad720fb91cdfa6a5a3e57905fee6911450ae66d28331b2c2ca7b53b545d4b3c78a0dfb7.png/{token}`  _(calls: 2, status: 200:2)_
  - Response: `PNG

   IHDR    	   1n dIDATx콉{UU[n]..@ڪr.EEQPfL"CdaL $L2  NrwZ{}νͳB{9}>rwdDSw!0=?`M?;'w>f[;6qb~Fԫ_;)84q?'k揁S4}ZzL=-S/*_ɾ7Yi%[{@jl+OCޟ_疿z7<
LΣ/g?7Y*ONpuƝd7KVӮbr'4...`
- **GET** `https://conteudoava.unicesumar.edu.br/display/arquivo-banner-web/213a6922448cb36745c2542e5425d79efb7f0a32c88fe4f3d8a89e102c56307cb8a846b8eb57251b182cbfe9c91d20b4e97756d25f6e1782a0d32d99e8fe1027.png/{token}`  _(calls: 2, status: 200:2)_
  - Response: `PNG

   IHDR    	   1n IDATxkWVs*%03f&30`n&E00ۡx `bB*H9G*`S.0	I#iF#ZR~OcIQ RO{^^~,Db$Iys#BpD}3w;sD)'""3=.r)DY% "Ns)\SSyBgcc1岉9Bާ7DR
˹s2S!2BD>8YGINDB`f"D^8...`
- **GET** `https://conteudoava.unicesumar.edu.br/display/arquivo-banner-web/918cf4a8ff0f2b3d947047759fe0de4413bb235c6c678ac4d7c83e807a0c48bad1a67377f76c5c4d0d5578a37e9646e3a7141da07b33ea890311a59c205256c1.png/{token}`  _(calls: 2, status: 200:2)_
  - Response: `PNG

   IHDR    	   1n PRIDATxT$r 3g2hCL2Qz0=xv2ϑ=wI[;;]?@ ݣwx܏zKkJ}}RοnW2Jmuk?ZzZ㸮8[.c~R?>Ǿmug/+m:ϯ9γ{~}8<\g;~ڼx~/Z]W5Um~F=QhzJϷh?tw5k~Q>F7|~]6e>u׵豜]t}k:n| Zژ;A6q<_zo"~K...`
- **GET** `https://conteudoava.unicesumar.edu.br/display/arquivo-banner-web/acc87654af83d997499bb549c8aaeafef7ee29a0714ad9a767f6847d27361e424265ff839dc035dcf07a9f512d6532387b6e840ae2efa7076e06475a73639c62.png/{token}`  _(calls: 2, status: 200:2)_
  - Response: `PNG

   IHDR     g   o EIDATxڌɒ$I-DdeuZ44ӄyyc<D8hЃwEUqfUl$EzzD@ Z~(&~*~(	MH %p	ф.BtBI]AI#K0ci#$t+qH0 Ip#&tF/)W`a@"`Eo??'{678@;z@~B̈+	n+"Æ...`
- **GET** `https://conteudoava.unicesumar.edu.br/display/arquivo-geral/f869cf0d69209ad57ae9d433d6a4c8e5cdf423aad34e5aa2bfc2541680f6c90847fdf124fdf592921f3b09faef622914802a31068d4d1cdb2e048773328db95b.jpg/{token}`  _(calls: 2, status: 200:2)_
  - Response: `PNG

   IHDR         X   sRGB     IDATx^lWlu%2ozo*n nCɠFFH1Ҍ|̐@)Q5Ҁ$@  võCw?oʽ&73975^Ue瞽k;CۍeC/`8 >1x0p X0rɛk\n.k[=g\'x p7` ?εP	A}y%}}yp-\nx{\{r˧Ϳ#QQ...`
- **GET** `https://studeoapi.unicesumar.edu.br/atendimento-api-controller/api/filtro-comunicado`  _(calls: 2, status: 200:2)_
  - Response: `[]`
- **GET** `https://studeoapi.unicesumar.edu.br/atendimento-api-controller/api/atendimento/qtd-mensagens-nao-lidas`  _(calls: 2, status: 200:2)_
  - Response: `[{"situacao": "COMUNICADO", "qtdMensagem": 5}]`
- **GET** `https://studeoapi.unicesumar.edu.br/atendimento-api-controller/api/atendimento?aba&mediador&novasPrimeiro&pageOffset&startIndex`  _(calls: 2, status: 200:2)_
  - Response: `[{"id": 5021782, "nmDestinatario": "ELAINE IGNACIO MOREIRA", "cdUsuario": null, "ultimoTexto": "<p>Ol&aacute;, estudante!&nbsp;</p>\n\n<p>&nbsp;</p>\n\n<p>J&aacute; pensou em estudar espanhol direto d...`
- **GET** `https://studeoapi.unicesumar.edu.br/ambiente-api-controller/api/aluno/disciplina/matriculados`  _(calls: 2, status: 200:2)_
  - Response: `[{"tpMatricula": "MATRICULADO", "tpDetalhe": "Nao curricular", "idDisciplina": 312376, "nmDisciplina": "GIRO EAD", "cdShortname": "MDL_AC_7158", "flAtivo": true, "dhLiberar": null, "ano": 2026, "semes...`
- **POST** `https://studeoapi.unicesumar.edu.br/objeto-ensino-api-controller/api/questionario/afazer/`  _(calls: 2, status: 200:2)_
  - Request: `{"cdShortname": ["MDL_AC_7158", "MDL_AC_19885", "2026_26_EGRAD_ADSIS5E-51_EGRAD_GRAD_080_0026", "2026_26_EGRAD_ADSIS5E-51_EGRAD_GRAD_080_0523", "MDL_AC_26697", "MDL_AC_26453", "MDL_AC_26482", "MDL_AC_...`
  - Response: `[{"somaAtividades": 2, "proximaAtividade": 1773629999000, "shortname": "2026_26_EGRAD_ADSIS5E-51_EGRAD_GRAD_080_0523"}, {"somaAtividades": 1, "proximaAtividade": 1777258799000, "shortname": "MDL_AC_26...`
- **POST** `https://studeoapi.unicesumar.edu.br/auth-api-controller/auth/token/revoke`  _(calls: 1, status: 200:1)_
  - Request: `{"token": "eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIyNTA1MDMyNS01IiwiZGF0Ijp7InJ1dCI6bnVsbCwiZGVmIjp7Ik5FU1QiOiJBTFVOTyJ9LCJ0cnMiOmZhbHNlLCJlbWwiOiJSQTI1MDUwMzI1NUBFQUQuQ0VTVU1BUi5CUiIsIml0ZyI6dHJ1ZSwicm9sIjp7...`