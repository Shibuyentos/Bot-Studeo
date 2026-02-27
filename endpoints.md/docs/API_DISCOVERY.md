# API_DISCOVERY (gerado automaticamente)

## Resumo
- **Endpoints únicos:** 46
- **Total de chamadas observadas:** 196
- **Hosts first-party:** 5

## Observações
- Arquivo gerado a partir de tráfego capturado (HAR ou inventário prévio).
- Tokens/cookies/IDs foram normalizados e mascarados.
- `OPTIONS` (CORS preflight) descartado por padrão.
- Assets estáticos (JS, CSS, imagens, fontes) descartados por padrão.
- Analytics e trackers de terceiros descartados por padrão.

## Hosts
- `studeoapi.unicesumar.edu.br` — 37 endpoints, 172 chamadas
- `conteudoava.unicesumar.edu.br` — 5 endpoints, 10 chamadas
- `api-financial.vitru.com.br` — 1 endpoints, 6 chamadas
- `studeo.unicesumar.edu.br` — 2 endpoints, 6 chamadas
- `api-areasegura.vitru.com.br` — 1 endpoints, 2 chamadas

## Inventário de Endpoints (por host e controller)

### studeoapi.unicesumar.edu.br

#### auth-api-controller
- **GET** `/auth-api-controller/auth/token/time-info` _(calls: 17 | 200:17)_
  - **Response Body:** `{"datetime": "2026-02-26T20:55:21.841-0300", "offset": -180, "timezone": "-0300", "timezoneId": "America/Sao_Paulo", "timestamp": 1772150121841}`
- **GET** `/auth-api-controller/api/rota-app/autorizacao` _(calls: 6 | 200:6)_
  - **Response Body:** `{"access.login": true, "app.nest.aluno.ambiente.negocia-dividas.index": true, "app.nest.aluno.ambiente.acomp-curso.list": true, "app.nest.admin.cpa.tag": true, "app.forms.elements": true, "app.nest.aluno.ambiente.servicos.list": true, "app.nest.aluno.ambiente.material-digital-layout": true, "app.nes...`
- **GET** `/auth-api-controller/api/parametro/autorizacao` _(calls: 6 | 0:1, 200:5)_
  - **Response Body:** `{"PARAM_FORUM_NOTA_MAX": "40", "PARAM_SISTEMA_RUBINHO": "700", "PARAM_PERIODO_CONSULTA_PLANO_ESTUDO_GERAL": "7", "PARAM_PAGINA_INICIAL_TEMPLATE_NAME": "template-aluno", "QUESTIONARIO_VERIFICA_INADIMPLENCIA": "S", "PARAM_ALUNO_FALE_MEDIADOR": "true", "PARAM_BOTAO_VISUALIZAR_CERTIFICADO_CONCLUSAO": "t...`
- **POST** `/auth-api-controller/auth/token/create` _(calls: 4 | 200:4)_
  - **Request Body:** `{"username": "80070107939", "password": "Renann1."}`
- **GET** `/auth-api-controller/api/permissao/autorizacao` _(calls: 4 | 200:4)_
  - **Response Body:** `{"MENU_LATERAL_ALUNO_SERVICOS_ATUALIZAR_DADOS_CADASTRAIS": true, "MENU_LATERAL_ALUNO_DIPLOMA_DIGITAL": true, "MENU_LATERAL_CERTIFICADO_ALUNOS_CONCLUIDOS": true, "MENU_LATERAL_ALUNO_BIBLIOTECAS_BIBLIOTECA_ZBRA": true, "MENU_LATERAL_ALUNO_MEU_PAPEL_NO_MUNDO": true, "MENU_LATERAL_ALUNO_MEU_CURSO_DISCIP...`
- **POST** `/auth-api-controller/auth/token/renew` _(calls: 2 | 200:2)_
  - **Request Body:** `{"refreshToken": "eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIyNTA1MDMyNS01IiwiZGF0Ijp7InJ1dCI6bnVsbCwiZGVmIjp7Ik5FU1QiOiJBTFVOTyJ9LCJ0cnMiOmZhbHNlLCJlbWwiOiJSQTI1MDUwMzI1NUBFQUQuQ0VTVU1BUi5CUiIsIml0ZyI6dHJ1ZSwicm9sIjp7Ik5FU1QiOlsiQUxVTk8iXX0sImVtZyI6IlJBMjUwNTAzMjU1QEVBRC5DRVNVTUFSLkJSIn0sImlzcyI6Ik5FU1QiLCJle...`
  - **Response Body:** `{"token": "eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIyNTA1MDMyNS01IiwiZGF0Ijp7InJ1dCI6bnVsbCwiZGVmIjp7Ik5FU1QiOiJBTFVOTyJ9LCJ0cnMiOmZhbHNlLCJlbWwiOiJSQTI1MDUwMzI1NUBFQUQuQ0VTVU1BUi5CUiIsIml0ZyI6dHJ1ZSwicm9sIjp7Ik5FU1QiOlsiQUxVTk8iXX0sImVtZyI6IlJBMjUwNTAzMjU1QEVBRC5DRVNVTUFSLkJSIn0sImlzcyI6Ik5FU1QiLCJleHAiOjE3...`
- **POST** `/auth-api-controller/auth/token/revoke` _(calls: 1 | 200:1)_
  - **Request Body:** `{"token": "eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIyNTA1MDMyNS01IiwiZGF0Ijp7InJ1dCI6bnVsbCwiZGVmIjp7Ik5FU1QiOiJBTFVOTyJ9LCJ0cnMiOmZhbHNlLCJlbWwiOiJSQTI1MDUwMzI1NUBFQUQuQ0VTVU1BUi5CUiIsIml0ZyI6dHJ1ZSwicm9sIjp7Ik5FU1QiOlsiQUxVTk8iXX0sImVtZyI6IlJBMjUwNTAzMjU1QEVBRC5DRVNVTUFSLkJSIn0sImlzcyI6Ik5FU1QiLCJleHAiOjE3...`

#### ambiente-api-controller
- **GET** `/ambiente-api-controller/api/aluno/disciplina/curricular/false` _(calls: 8 | 200:8)_
  - **Response Body:** `[{"tpMatricula": "MATRICULADO", "tpDetalhe": "Nao curricular", "idDisciplina": 312376, "nmDisciplina": "GIRO EAD", "cdShortname": "MDL_AC_7158", "flAtivo": true, "dhLiberar": null, "ano": 2026, "semestre": 99, "cdDisciplina": "7158", "cdTurma": "7158", "flCurricular": false, "flDestaque": false, "fl...`
- **GET** `/ambiente-api-controller/api/internet-patrocinada/validar-acesso` _(calls: 4 | 200:4)_
  - **Response Body:** `{"flInternet": true, "dsMensagem": "Ola aluno! Sua internet patrocinada está ativa."}`
- **GET** `/ambiente-api-controller/api/aluno/disciplina/active` _(calls: 4 | 200:4)_
  - **Response Body:** `["1"]`
- **GET** `/ambiente-api-controller/api/controle-servico/ativa/BANNER/WEB` _(calls: 4 | 200:4)_
  - **Response Body:** `{"responseStatus": "OK", "responseMessage": null, "entity": true}`
- **GET** `/ambiente-api-controller/api/aluno/disciplina/curricular/true` _(calls: 4 | 200:4)_
  - **Response Body:** `[{"tpMatricula": "Matriculado", "tpDetalhe": "Curricular", "idDisciplina": 766981, "nmDisciplina": "ANÁLISE E PROJETO ORIENTADO A OBJETOS", "cdShortname": "2026_26_EGRAD_ADSIS5E-51_EGRAD_GRAD_080_0026", "flAtivo": true, "dhLiberar": null, "ano": 2026, "semestre": 51, "cdDisciplina": "EGRAD_GRAD_080_...`
- **GET** `/ambiente-api-controller/api/banner/active/homeBannerDisciplinas` _(calls: 4 | 200:4)_
  - **Response Body:** `[{"dhInsert": 1748867488183, "dhUpdate": 1751457679523, "dsBanner": "PREPARE-SE", "dhInicio": 1748746800000, "dhFim": 1782874740000, "dsImagemWeb": "acc87654af83d997499bb549c8aaeafef7ee29a0714ad9a767f6847d27361e424265ff839dc035dcf07a9f512d6532387b6e840ae2efa7076e06475a73639c62.png", "dsImagemApp": n...`
- **GET** `/ambiente-api-controller/api/banner/search/active` _(calls: 4 | 200:4)_
  - **Response Body:** `[{"idBanner": 1510, "dsBanner": "Alteração de CNPJ - GRAD. EAD", "dsImagemWeb": "918cf4a8ff0f2b3d947047759fe0de4413bb235c6c678ac4d7c83e807a0c48bad1a67377f76c5c4d0d5578a37e9646e3a7141da07b33ea890311a59c205256c1.png", "dsImagemApp": "11b537b3905374eab297031be09d84444225fb77441176758a15bce7eda7dee57816...`
- **GET** `/ambiente-api-controller/api/aluno/disciplina/afazer` _(calls: 4 | 200:4)_
  - **Response Body:** `{"somaTotal": 70}`
- **GET** `/ambiente-api-controller/api/aluno/disciplina/matriculados` _(calls: 2 | 200:2)_
  - **Response Body:** `[{"tpMatricula": "MATRICULADO", "tpDetalhe": "Nao curricular", "idDisciplina": 312376, "nmDisciplina": "GIRO EAD", "cdShortname": "MDL_AC_7158", "flAtivo": true, "dhLiberar": null, "ano": 2026, "semestre": 99, "cdDisciplina": "7158", "cdTurma": "7158", "flCurricular": false, "flDestaque": false, "fl...`

#### log-acesso-api-controller
- **POST** `/log-acesso-api-controller/api/evento/` _(calls: 21 | 200:21)_
  - **Request Body:** `{"idSessao": {"id": 866574440}, "idTipoEvento": {"dsTipoEvento": "LOGIN"}, "idTipoConteudo": {"dsTipoConteudo": "LOGIN"}, "cdUsuario": "25023123-2", "cdCurso": "PGO_CST_ADSIS", "cdShortname": null, "cdConteudo": null, "cdTela": "LOGIN", "cdItemTela": null, "vlStatus": 1, "dsRetorno": null}`
  - **Response Body:** `{"id": 10008287024, "idSessao": {"id": 866605521, "idFormaAcesso": null, "cdUsuario": null, "dsDispositivoAcesso": null, "dsBrowser": null, "vlLatitude": null, "vlLongitude": null, "token": null}, "idTipoEvento": {"id": 51, "dsTipoEvento": "LOGIN"}, "idTipoConteudo": {"id": 46, "dsTipoConteudo": "LO...`
- **POST** `/log-acesso-api-controller/api/sessao/` _(calls: 4 | 200:4)_
  - **Request Body:** `{"cdUsuario": "25023123-2", "idFormaAcesso": {"dsFormaAcesso": "WEB"}, "dsBrowser": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)", "vlLatitude": null, "vlLongitude": null, "token": "eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIyNTAyMzEyMy0yIiwiZGF0Ijp7InJ1dCI6bnVsbCwiZGVmIjp7...`
  - **Response Body:** `{"id": 866605521, "idFormaAcesso": {"id": 2, "dsFormaAcesso": "WEB"}, "cdUsuario": "25050325-5", "dsDispositivoAcesso": null, "dsBrowser": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)", "vlLatitude": null, "vlLongitude": null, "token": "eyJhbGciOiJSUzI1NiJ9.eyJzd...`
- **POST** `/log-acesso-api-controller/api/navegador-detalhe/` _(calls: 4 | 200:4)_
  - **Request Body:** `{"idSessao": {"id": 866574440}, "dsBrowser": "Google Chrome or Chromium", "dsIPAddress": "0.0.0.0"}`
  - **Response Body:** `{"id": 677521526, "idNavegadorDetalhe": 677521526, "idSessao": {"id": 866605521, "idFormaAcesso": null, "cdUsuario": null, "dsDispositivoAcesso": null, "dsBrowser": null, "vlLatitude": null, "vlLongitude": null, "token": null}, "dsBrowser": "Google Chrome or Chromium", "dsIPAddress": "172.17.20.2", ...`

#### atendimento-api-controller
- **GET** `/atendimento-api-controller/api/atendimento/push` _(calls: 13 | 200:13)_
  - **Response Body:** `{"list": [{"idConversa": 5012280, "qtaMsg": 1, "aviso": true, "finalizada": false, "solicitaFinalizar": false, "mensagem": null}, {"idConversa": 5012313, "qtaMsg": 1, "aviso": true, "finalizada": false, "solicitaFinalizar": false, "mensagem": null}, {"idConversa": 5016460, "qtaMsg": 1, "aviso": true...`
- **GET** `/atendimento-api-controller/api/atendimento/push?init` _(calls: 6 | 200:6)_
  - **Response Body:** `{"list": [{"idConversa": 5012280, "qtaMsg": 1, "aviso": true, "finalizada": false, "solicitaFinalizar": false, "mensagem": null}, {"idConversa": 5012313, "qtaMsg": 1, "aviso": true, "finalizada": false, "solicitaFinalizar": false, "mensagem": null}, {"idConversa": 5016460, "qtaMsg": 1, "aviso": true...`
- **GET** `/atendimento-api-controller/api/filtro-comunicado` _(calls: 2 | 200:2)_
  - **Response Body:** `[]`
- **GET** `/atendimento-api-controller/api/atendimento/qtd-mensagens-nao-lidas` _(calls: 2 | 200:2)_
  - **Response Body:** `[{"situacao": "COMUNICADO", "qtdMensagem": 5}]`
- **GET** `/atendimento-api-controller/api/atendimento?aba&mediador&novasPrimeiro&pageOffset&startIndex` _(calls: 2 | 200:2)_
  - **Response Body:** `[{"id": 5021782, "nmDestinatario": "ELAINE IGNACIO MOREIRA", "cdUsuario": null, "ultimoTexto": "<p>Ol&aacute;, estudante!&nbsp;</p>\n\n<p>&nbsp;</p>\n\n<p>J&aacute; pensou em estudar espanhol direto da Espanha, com despesas pagas?&nbsp;</p>\n\n<p>O <strong>Santander Top Espanha 2026</strong> vai lev...`

#### controle-acesso-api-controller
- **GET** `/controle-acesso-api-controller/api/usuario-foto/{id}` _(calls: 6 | 200:2, 204:4)_
  - **Response Body:** `{"idUsuarioFoto": 20803240, "cdUsuario": "25050325-5", "idCentralAnexo": 20803240}`
- **GET** `/controle-acesso-api-controller/api/usuario-regra/existe-regra` _(calls: 4 | 200:2, 204:2)_
- **GET** `/controle-acesso-api-controller/api/usuario/info-login` _(calls: 4 | 200:4)_
  - **Response Body:** `{"id": 2494641, "cdUsuario": "25050325-5", "nmUsuario": "Kauann Gabriel Shibuya", "dsEmail": "RA250503255@EAD.CESUMAR.BR", "dhUltimoAcesso": 1772150120322, "nmPerfil": "ALUNO", "curso": null, "modalidade": null, "cpf": "80070107939", "unidadeAssociada": {"id": 371, "idUnidadeAssociada": 371, "cdUnid...`
- **GET** `/controle-acesso-api-controller/api/usuario/usuarios/{id}` _(calls: 2 | 200:2)_
- **GET** `/controle-acesso-api-controller/api/usuario-regra` _(calls: 2 | 200:2)_
  - **Response Body:** `[{"id": 91798479, "idUsuarioRegra": 91798479, "usuario": {"id": 2494641, "nmUsuario": "Kauann Gabriel Shibuya", "cdUsuario": "25050325-5", "dhInsert": 1732349560695, "dhUpdate": 1764569372981}, "regra": {"id": 178, "cdRegra": "QUIZ_NPS_25_SEMESTRE2_2", "nmRegra": "Pesquisa de Satisfação", "flAtivo":...`

#### lyceum-api-controller
- **GET** `/lyceum-api-controller/api/portal-parceiro/grupo` _(calls: 4 | 200:4)_
  - **Response Body:** `["0"]`
- **GET** `/lyceum-api-controller/api/servicos/dados-cadastrais` _(calls: 2 | 200:2)_
- **GET** `/lyceum-api-controller/api/vem-comigo/permissao` _(calls: 2 | 204:2)_
- **GET** `/lyceum-api-controller/api/servico-dp-especial/` _(calls: 2 | 200:2)_
  - **Response Body:** `[]`

#### objeto-ensino-api-controller
- **GET** `/objeto-ensino-api-controller/api/plano-estudo/disciplinas-usuario` _(calls: 4 | 200:2, 204:2)_
  - **Response Body:** `[{"dhInicial": 1771930800000, "dhFinal": 1771988340000, "dsPlanoDeEstudoTipoEvento": "Aula", "dsPlanoDeEstudoSubTipoEvento": "AULA", "dsPlanoDeEstudoTipoAlerta": "Aula", "tpCor": "success", "nmDisciplina": "MENTALIDADE CRIATIVA E EMPREENDEDORA", "cdShortname": "2026_26_EGRAD_ADSIS5E-51_EGRAD_GRAD_08...`
- **POST** `/objeto-ensino-api-controller/api/questionario/afazer/` _(calls: 2 | 200:2)_
  - **Request Body:** `{"cdShortname": ["MDL_AC_7158", "MDL_AC_19885", "2026_26_EGRAD_ADSIS5E-51_EGRAD_GRAD_080_0026", "2026_26_EGRAD_ADSIS5E-51_EGRAD_GRAD_080_0523", "MDL_AC_26697", "MDL_AC_26453", "MDL_AC_26482", "MDL_AC_26672"]}`
  - **Response Body:** `[{"somaAtividades": 2, "proximaAtividade": 1773629999000, "shortname": "2026_26_EGRAD_ADSIS5E-51_EGRAD_GRAD_080_0523"}, {"somaAtividades": 1, "proximaAtividade": 1777258799000, "shortname": "MDL_AC_26482"}, {"somaAtividades": 1, "proximaAtividade": 1777258799000, "shortname": "MDL_AC_26672"}, {"soma...`

#### iam-api-controller
- **GET** `/iam-api-controller/api/usuario/quantidade-usuarios` _(calls: 4 | 200:4)_
  - **Response Body:** `{"cpf": "80070107939", "qtdUsuario": "2"}`

#### central-anexo-api-controller
- **GET** `/central-anexo-api-controller/api/anexo/findBy/{id}` _(calls: 2 | 200:2)_
  - **Response Body:** `{"id": 20803240, "nmOriginalArquivo": "IMG_2057.jpg", "dsPath": "arquivo-geral", "cdHash": "f869cf0d69209ad57ae9d433d6a4c8e5cdf423aad34e5aa2bfc2541680f6c90847fdf124fdf592921f3b09faef622914802a31068d4d1cdb2e048773328db95b", "tamanhoArquivo": "0", "cdExtensao": "jpg", "dhInsert": 1750533395691, "dhUpd...`


### conteudoava.unicesumar.edu.br

#### display/arquivo-banner-web
- **GET** `/display/arquivo-banner-web/6f1842cd8abb5bab69fa64f49503631b022bf2a26777c4f3a00eb5557ad720fb91cdfa6a5a3e57905fee6911450ae66d28331b2c2ca7b53b545d4b3c78a0dfb7.png/{token}` _(calls: 2 | 200:2)_
  - **Response Body:** `PNG

   IHDR    	   1n dIDATx콉{UU[n]..@ڪr.EEQPfL"CdaL $L2  NrwZ{}νͳB{9}>rwdDSw!0=?`M?;'w>f[;6qb~Fԫ_;)84q?'k揁S4}ZzL=-S/*_ɾ7Yi%[{@jl+OCޟ_疿z7<
LΣ/g?7Y*ONpuƝd7KVӮbr'4...`
- **GET** `/display/arquivo-banner-web/213a6922448cb36745c2542e5425d79efb7f0a32c88fe4f3d8a89e102c56307cb8a846b8eb57251b182cbfe9c91d20b4e97756d25f6e1782a0d32d99e8fe1027.png/{token}` _(calls: 2 | 200:2)_
  - **Response Body:** `PNG

   IHDR    	   1n IDATxkWVs*%03f&30`n&E00ۡx `bB*H9G*`S.0	I#iF#ZR~OcIQ RO{^^~,Db$Iys#BpD}3w;sD)'""3=.r)DY% "Ns)\SSyBgcc1岉9Bާ7DR
˹s2S!2BD>8YGINDB`f"D^8...`
- **GET** `/display/arquivo-banner-web/918cf4a8ff0f2b3d947047759fe0de4413bb235c6c678ac4d7c83e807a0c48bad1a67377f76c5c4d0d5578a37e9646e3a7141da07b33ea890311a59c205256c1.png/{token}` _(calls: 2 | 200:2)_
  - **Response Body:** `PNG

   IHDR    	   1n PRIDATxT$r 3g2hCL2Qz0=xv2ϑ=wI[;;]?@ ݣwx܏zKkJ}}RοnW2Jmuk?ZzZ㸮8[.c~R?>Ǿmug/+m:ϯ9γ{~}8<\g;~ڼx~/Z]W5Um~F=QhzJϷh?tw5k~Q>F7|~]6e>u׵豜]t}k:n| Zژ;A6q<_zo"~K...`
- **GET** `/display/arquivo-banner-web/acc87654af83d997499bb549c8aaeafef7ee29a0714ad9a767f6847d27361e424265ff839dc035dcf07a9f512d6532387b6e840ae2efa7076e06475a73639c62.png/{token}` _(calls: 2 | 200:2)_
  - **Response Body:** `PNG

   IHDR     g   o EIDATxڌɒ$I-DdeuZ44ӄyyc<D8hЃwEUqfUl$EzzD@ Z~(&~*~(	MH %p	ф.BtBI]AI#K0ci#$t+qH0 Ip#&tF/)W`a@"`Eo??'{678@;z@~B̈+	n+"Æ...`

#### display/arquivo-geral
- **GET** `/display/arquivo-geral/f869cf0d69209ad57ae9d433d6a4c8e5cdf423aad34e5aa2bfc2541680f6c90847fdf124fdf592921f3b09faef622914802a31068d4d1cdb2e048773328db95b.jpg/{token}` _(calls: 2 | 200:2)_
  - **Response Body:** `PNG

   IHDR         X   sRGB     IDATx^lWlu%2ozo*n nCɠFFH1Ҍ|̐@)Q5Ҁ$@  võCw?oʽ&73975^Ue瞽k;CۍeC/`8 >1x0p X0rɛk\n.k[=g\'x p7` ?εP	A}y%}}yp-\nx{\{r˧Ϳ#QQ...`


### api-financial.vitru.com.br

#### api/rest
- **GET** `/api/rest/billing/method/renegotiation/{id}/LY_PGO_CST_ADSIS` _(calls: 6 | 0:1, 200:5)_
  - **Response Body:** `{"type": "OLD"}`


### studeo.unicesumar.edu.br

#### root
- **GET** `/` _(calls: 3 | 200:3)_
  - **Response Body:** `<!DOCTYPE html> <html lang="pt-BR" data-ng-app="app" ng-strict-di ng-controller="AppCtrl"> <head> <meta http-equiv="content-type" content="text/html;charset=UTF-8"/> <meta charset="utf-8"/> <title ncy...`
- **GET** `/{token}` _(calls: 3 | 200:3)_
  - **Response Body:** `{"short_name": "Studeo", "name": "STUDEO - SEU AMBIENTE VIRTUAL DE APRENDIZAGEM", "icons": [{"src": "br/edu/unicesumar/web-angular-layout/src/pages/ico/s-48.0460f2e9.png", "type": "image/png", "sizes": "48x48"}, {"src": "br/edu/unicesumar/web-angular-layout/src/pages/ico/s-60.6c7f82a6.png", "type": ...`


### api-areasegura.vitru.com.br

#### security/check
- **POST** `/security/check` _(calls: 2 | 200:2)_
  - **Request Body:** `{"username": "80070107939", "birthDay": "05/05/2007"}`

