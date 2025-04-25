\name{TechSolution-package}
\alias{TechSolution-package}
\docType{package}
\title{TechSolution: Ferramentas para ingestão, análise e dashboard de dados do agronegócio}
\description{
TechSolution fornece funções para coletar dados de FAOSTAT e COMEXSTAT, pré-processar data.frames,
treinar modelos de perdas na colheita e gerar um dashboard Shiny integrado ao Oracle.
}

\details{
O pacote inclui:
\itemize{
  \item ingest\_faostat(): coleta dados FAOSTAT e grava raw no Oracle;
  \item ingest\_comexstat(): coleta dados COMEXSTAT e grava raw no Oracle;
  \item drop\_missing(), fill\_defaults(), normalize\_numeric(), encode\_categorical(): rotinas de limpeza e transformação;
  \item train\_harvest\_loss(), predict\_harvest\_loss(): modelagem de perdas na colheita com caret;
  \item run\_dashboard(): dashboard Shiny de insumos agrícolas.
}
Para mais detalhes sobre o formato Rd, consulte o manual de R Extensions :contentReference[oaicite:1]{index=1}.
}

\author{
  Guilherme Pires de Sotti Machado \\ 
  \email{gpiresmachado@hotmail.com} \\ 
  \role{aut,cre}
}

\keyword{package}
