
#install.packages("leaflet")
#install.packages("leaflet.extras")

library(shiny)
library(tidyverse)
library(shinyWidgets)
library(leaflet)
library(leaflet.extras)


#loading the final dataset resulting from the 
load("Finaler_Datensatz_25.RData")

#uncomment the following line to load dataset faster
#final <- head(final, 500)


#create a data frame jsut containing the locations
places <- group_by(final, Ort) %>%
  summarise(n=n())

# Define UI for application that draws a histogram
ui <- fluidPage(
  
  # Application title
  titlePanel("Defective & Registered Cars"),
  
  
  # Show a plot of the generated distribution
  mainPanel(width = "100%",
            
            #input modules based on the date, location and car manufacturer
            wellPanel(width = "90%",
                      titlePanel("Filters for Displaying Registrations over Time"),
                      fluidRow(
                        column(width = 6, 
                               
                               dateRangeInput("registration", 
                                              label = "Choose the time period.",
                                              start = min(final$Zulassung),
                                              end = max(final$Zulassung),
                                              min = min(final$Zulassung),
                                              max = max(final$Zulassung),
                                              startview = "year",
                                              format = "yyyy-mm-dd"),
                               
                               radioButtons("manufacturer", 
                                            label = "Showcase the data by", 
                                            choices = c("Car manufacturer", "Engine manufacturer"),
                                            select = "Car manufacturer")
                        ),
                        
                        column(width= 6,
                               
                               pickerInput("location",
                                           label = "Choose the location to observe",
                                           choices =  c("All", places$Ort),
                                           selected = "All"),
                               
                               conditionalPanel("input.manufacturer == 'Car manufacturer'",
                                                
                                                selectInput("car_manufacturer", 
                                                            label = "Choose the Car manufacturer",
                                                            choices = c("All", 1, 2),
                                                            selected = "All")
                               ),
                               
                               conditionalPanel("input.manufacturer == 'Engine manufacturer'",
                                                
                                                selectInput("engine_manufacturer", 
                                                            label = "Choose the Engine manufacturer",
                                                            choices = c("All", 101, 102, 103, 104),
                                                            selected = "All")
                               )
                        )
                      ),
                      
                      
                      # Output of the plot related to the registration over the time
                      plotOutput("registration",
                                 width = "100%"  
                      )
            ),  
            
            wellPanel(width = "90%",
                      titlePanel("Filters for Displaying Geographical distribution"),
                      fluidRow(
                        #the input given by the user for the heatmap
                        column(6,
                               dateRangeInput("heatmap", 
                                              label = "Choose the time period",
                                              start = min(final$Zulassung),
                                              end = max(final$Zulassung),
                                              min = min(final$Zulassung),
                                              max = max(final$Zulassung)),
                               
                               radioButtons("manufacturer2", 
                                            label = "Showcase the data by", 
                                            choices = c("Car manufacturer", "Engine manufacturer"),
                                            select = "Car manufacturer")
                               
                               
                        ),
                        #the user chooses whether to display the density numerically though clusters, or graphically through a heatmap
                        column(6,
                               selectInput("mapDisplay",
                                           label = "Select display mode of map",
                                           choices = c("Marker Clusters", "Heatmap", "Heatmap with Marker Clusters"),
                                           selected = "Heatmap with Marker Clusters"
                               ),
                               conditionalPanel("input.mapDisplay == 'Heatmap' | input.mapDisplay == 'Heatmap with Marker Clusters'",
                                                
                                                numericInput("fehleranzahl",
                                                             label = "Choose mininum amount of defective cars",
                                                             value = 20,
                                                             min = 1,
                                                             max = 10000,
                                                             step = 1)
                               ),
                               conditionalPanel("input.manufacturer2 == 'Car manufacturer'",
                                                
                                                selectInput("car_manufacturer2", 
                                                            label = "Choose the Car manufacturer",
                                                            choices = c("All", 1, 2),
                                                            selected = "All")
                               ),
                               
                               conditionalPanel("input.manufacturer2 == 'Engine manufacturer'",
                                                
                                                selectInput("engine_manufacturer2", 
                                                            label = "Choose the Engine manufacturer",
                                                            choices = c("All", 101, 102, 103, 104),
                                                            selected = "All")
                               )
                               
                            )
                        ),
                      
                      titlePanel(
                        h4("Geographical Distribution of Cars")
                      ),
                      titlePanel(
                        h6("Click or scroll on the clusters to zoom in. Click the markers to reveal information about the car.")
                      ),
                      mainPanel(width = "90%",
                                
                                # Show the distribution of registered cars on a map
                                leafletOutput("gerMap", 
                                              width = "90%",
                                              height = "650px")
                      )
            ),
            wellPanel(width = "90%",
                      titlePanel("Tabular Representation of Data"),
                      #user has the choice of using the table to further explore the map, or to search for items individually
                      selectInput("mapFilters", 
                                  label = "Use filters from Map Display?",
                                  choices = c("Use Map Filters", "Display Unfiltered Dataset"),
                                  selected = "Use Map Filters"),
                      mainPanel(width = "100%",
                                dataTableOutput("table")    
                      )
                      
            )
            
  )
)

# Define server logic 
server <- function(input, output) {
  
  
  #filter dataset for sorting cars by car manufacturer
  registration <- reactive({
    
    count <- filter(final, Zulassung >= input$registration[1] & Zulassung <= input$registration[2])
    if (input$location != "All") {
      count <- filter(count, Ort == input$location)
    }
    if (input$car_manufacturer != "All") {
      count <- filter(count, Herstellernummer_Fahrzeug == input$car_manufacturer)
    }
    count$Zulassung <- format.Date(count$Zulassung, format = "%Y-%m")
    count$Zulassung <- as.character(count$Zulassung)
    count %>% group_by(Zulassung, Herstellernummer_Fahrzeug) %>%
      summarise(n = n())
    
  })
  #filter dataset for sorting cars by engine manufacturer
  registration_engine <- reactive({
    count <- filter(final, Zulassung >= input$registration[1] & Zulassung <= input$registration[2])
    if (input$location != "All") {
      count <- filter(count, Ort == input$location)
    }
    if (input$engine_manufacturer != "All") {
      count <- filter(count, Herstellernummer_Motor == input$engine_manufacturer)
    }
    count$Zulassung <- format.Date(count$Zulassung, format = "%Y-%m")
    count$Zulassung <- as.character(count$Zulassung)
    count %>% group_by(Zulassung, Herstellernummer_Motor) %>%
      summarise(n = n())
  })
  
  
  output$registration <- renderPlot({
    if (input$manufacturer == "Car manufacturer"){
      #create the plot based on the reactive registration() as bar plot
      p <- ggplot(data = registration(), aes(x = Zulassung, y = n, fill=factor(Herstellernummer_Fahrzeug))) +
        geom_bar(stat = "identity")
      #change the colours to shwocase the differen car manufacturer
      p <- p +scale_fill_manual(breaks = c("1", "2"),
                                values=c("#0B3B17", "#ff7f24"))
      #name axis, plot and legend
      p <- p + guides(fill = guide_legend(title="Car manufacturer"))
      p <- p + labs(x = "Date Range",
                    y = "Amount of Defective Cars registered",
                    title = "Registration of defective cars")
    } else {
      
      # create the plot based on the reactive registration_engine() as bar plot
      p <- ggplot(data = registration_engine(), aes(x = Zulassung, y = n, fill=factor(Herstellernummer_Motor))) +
        geom_bar(stat = "identity")
      # change the colours to shwocase the differen car manufacturer
      p <- p +scale_fill_manual(breaks = c("101", "102", "103", "104"),
                                values=c("#0B3B17", "#ff7f24", "#BEBEBE", "#a52a2a"))
      #name axis, plot and legend
      p <- p + guides(fill = guide_legend(title="Engine manufacturer"))
      p <- p + labs(x = "Date Range",
                    y = "Amount of Defective Cars registered",
                    title = "Registration of defective cars by Engine manufacturers")
      p
    }
    
    #format the plot in a nice format
    p <- p + theme(legend.position ="bottom", 
                   plot.title=element_text(size = 18, face="bold"), 
                   axis.title = element_text(size = 12),
                   legend.title.align = 0,
                   legend.direction = "horizontal",
                   legend.text = element_text(size = 12),
                   legend.title = element_text(size = 12, face = "bold"),
                   panel.background = element_rect(fill = "white", colour = "black"),
                   panel.grid.major.y = element_line(colour = "black", linetype = "solid"),
                   panel.grid.minor.y = element_line(colour = "black", linetype = "dotted"))
    p
    
  })
  
  filteredCars <- reactive ({
    #apply the filters as chosen by the user
    cars <- filter(final, Zulassung >= input$heatmap[1] & Zulassung <= input$heatmap[2])
    if (input$car_manufacturer2 != "All" & input$manufacturer2 == "Car manufacturer") {
      cars <- filter(cars, Herstellernummer_Fahrzeug == input$car_manufacturer2)
    }
    if (input$engine_manufacturer2 != "All" & input$manufacturer2 == "Engine manufacturer") {
      cars <- filter(cars, Herstellernummer_Motor == input$engine_manufacturer2)
    }
    cars
  }
  )
  
  
  
  #summarise locations to reflect number of defective cars per location
  heatmap <- reactive ({
    if (input$mapDisplay == 'Marker Clusters'  ) {
      #ensure that the column names stay the same by taking the first row of the final dataset...
      heat <- head(final,1)
      #adding an empty "fehleranzahl" column...
      heat$fehleranzahl <- NA
      #setting output to an empty df, so that nothing can be displayed on the heatmap
      heat <- filter(heat, FALSE)
    } else {
      heat <- filteredCars() %>%
        group_by(Ort, Laengengrad, Breitengrad) %>%
        summarise(fehleranzahl = n()) %>%
        #filter by number of registered cars
        filter(fehleranzahl >= input$fehleranzahl)
    }
    heat
  })
  
  markers <- reactive ({
    if(input$mapDisplay == 'Heatmap') {
      #if the markers are not supposed to be displayed, this returns an empty data frame that still has the same column names
      markers <- filter(final, FALSE) 
    } else {
      markers <- filteredCars()
    }
    markers
  })
  #prepare a dataset to be displayed as an overview in the table
  browseTable <- reactive({
    if (input$mapFilters ==  "Use Map Filters"){
      table <- filteredCars()
    } else {
      table <- final
    }
    #removing unneeded information:
    #the gps coordinates are not really relevant to humans
    #the car and motor manufacturer numbers are already represented in in ID_Fahrzeug and ID_Motor respectively
    table <- subset(table, select = -c(Laengengrad, Breitengrad, Herstellernummer_Fahrzeug, Herstellernummer_Motor))
    
    colnames(table) <- c("ID T1", "ID Engine", "ID Car", "Location of Registration", "Date of Registration", "Postcode")
    table
  })
  
  
  #using the leaflet package, we can visualise the data on a map
  output$gerMap <- renderLeaflet(
    #take the dataset of cars that results from the filters that the user chose.
    leaflet(data = filteredCars()) %>% 
      #adds a rendered map, by default openstreetmap
      addTiles() %>%
      #set the bounds of the map according to the coordinates of the locations
      fitBounds(min(final$Laengengrad),min(final$Breitengrad),max(final$Laengengrad),max(final$Breitengrad)) %>%
      #adds a heatmap representation of the density of registraiton of faulty cars
      addHeatmap(data = heatmap(), lng = ~Laengengrad, lat = ~Breitengrad, 
                 intensity = ~fehleranzahl, blur = 12, max = 10.0, radius = 8) %>%
      #postions one marker for each entry in the table
      addMarkers(data = markers(), ~Laengengrad, ~Breitengrad, 
                 #display large amounts of markers as clusters
                 clusterOptions = markerClusterOptions(), 
                 #display information about the car corresponding to the marker being clicked
                 popup = ~paste("Zugelassen in: <b> " ,Ort,"</b> <br/>",
                                "PLZ: ", Postleitzahl, "<br/>",
                                "Zulassung: ", Zulassung, "<br/>",
                                "ID_Fahrzeug: ", ID_Fahrzeug, "<br/>",
                                "ID_Motor: ", ID_Motor, "<br/>",
                                "ID_T1: ", ID_T1, "<br/>"
                 )
                 
      )
  )
  #display the dataset in a Data Table that the user can search, filter, and sort
  output$table <- renderDataTable(
    browseTable(),
    options = list(
      pageLength = 10
    )
  )
  
  
}

# Run the application 
shinyApp(ui = ui, server = server)

