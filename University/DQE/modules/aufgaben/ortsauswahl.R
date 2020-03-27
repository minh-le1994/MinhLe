ortsauswahl_ui <- function(id) {
  ns <- NS(id)
  
  tagList(
    data_selector_ui(
      id = ns("id_data_selector")
    ),
    actionButtonQW(
      inputId = ns("add_histogram"),
      label = NULL,
      icon = icon("area-chart"),
      tooltip = "Öffne Histogramm"
    )
  )
}

ortsauswahl <- function(input, output, session, .values) {
  
  ns <- session$ns
  
  data <- reactive({
    data_selector_return$data()
  })
  
  # Beispiel: Anfang
  histogram <- reactive({
    ggplot(data = mtcars, mapping = aes(x = mpg)) +
      geom_histogram(bins = nclass.Sturges(mpg)) +
      theme_bw()
  })
  
  observeEvent(input$add_histogram, {
    .values$viewer$append_tab(
      tab = tabPanel(
        title = "Histogram",
        value = "histogram",
        plotOutput(
          outputId = ns("histogram")
        )
      )
    )
  })
  
  output$histogram <- renderPlot({
    histogram()
  })
  # Beispiel: Ende
  
  data_selector_return <- callModule(
    module = data_selector,
    id = "id_data_selector",
    .values = .values
  )
}