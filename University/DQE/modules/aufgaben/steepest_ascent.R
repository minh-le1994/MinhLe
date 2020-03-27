steepest_ascent_ui <- function(id) {
  ns <- NS(id)
  
  tagList(
    data_selector_ui(
      id = ns("id_data_selector")
    )
  )
}

steepest_ascent <- function(input, output, session, .values) {
  
  ns <- session$ns
  
  data <- reactive({
    data_selector_return$data()
  })
  
  data_selector_return <- callModule(
    module = data_selector,
    id = "id_data_selector",
    .values = .values
  )
}