
# O poderiamos ter feito melhor  
  
Poderíamos implementar um processo de CI/CD para armazenar as chaves de acesso ao banco de dados, caso esse projeto fosse para um ambiente de produção. Evitando assim a exposição das credenciais de acesso ao banco de dados.  
  
Outro ponto está relacionado a escalabilidade do processo de scraping, na forma que foi desenvolvido, é possível apenas o escalonamento na vertical. Dependendo do contexto pode ser um problema.  

Para deixar o projeto completo, poderiamos também criar um SDK para facilitar o uso considerando disponibilizar para outros desenvolvedores.  
  
# Porque adotei as tecnologias 
Usei o mongoDB pelo fato de ser um banco muito comum e fácil para escalar, caso seja necessário só precisa criar novos nodes.  
Foi usado o docker-compose para orquestrar os serviços do mongo e da API, permitindo assim, melhor   
  
# Ponto de duvida  
O processo de predição das "appearances" ficou meio confuso, porque quando fazemos o scraping já coletamos o total de "appearances"  então não vejo necessidade de realizar a predição. Entretanto, mesmo assim vou fazer o calculo, então as entidades tem um novo campo para armazenar a predição.
