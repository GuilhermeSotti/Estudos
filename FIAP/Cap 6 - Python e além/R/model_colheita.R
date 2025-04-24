#' Treina modelo de classificação de perdas na colheita
#'
#' @param df data.frame com features e target binário
#' @param features character vector, nomes das colunas preditoras
#' @param target string, nome da coluna alvo (0/1)
#' @param out_path string, caminho para salvar o modelo (.rds)
#' @return objeto train do caret
#' @import caret
#' @export
train_harvest_loss <- function(df, features, target, out_path) {
  form <- stats::as.formula(paste(target, "~", paste(features, collapse = "+")))
  ctrl <- caret::trainControl(method = "cv", number = 5, classProbs = TRUE)
  model <- caret::train(form, data = df, method = "glm", family = "binomial", trControl = ctrl)
  saveRDS(model, out_path)
  return(model)
}

#' Gera probabilidades de alta perda
#'
#' @param model_path string, caminho do .rds previamente salvo
#' @param new_data data.frame com mesmas features usadas no treino
#' @return numeric vector de probabilidades
#' @export
predict_harvest_loss <- function(model_path, new_data) {
  model <- readRDS(model_path)
  probs <- predict(model, newdata = new_data, type = "prob")
  return(probs[, "1"])
}
