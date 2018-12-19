library(shiny)
library(plotly) # make data interactive
library(dplyr) 

# load dataset
df <- read.csv('R Files/R Files/Datasets/Scraped NBA Players.csv')

ui <- fluidPage(
  titlePanel("NBA Team Stats"), 
  sidebarLayout(
    sidebarPanel(selectInput("teamInput", "NBA TEAM",
                             choices=unique(df$TEAM))), # get unique NBA teams, order by name
    mainPanel(plotOutput("coolPlot"))
  )
)
server <- function(input, output){
  output$coolPlot <- renderPlot({
    # filter data by teams using dplyr
    filtered <- df %>%
                  filter(TEAM == input$teamInput)
    # plot data
    ggplotly(ggplot(filtered, aes(x=Player, y=PTS, label=PTS, col=Player, fill=Player)) +
      geom_col() +
      # put label on top of columns instead of inside
      geom_text(nudge_y = 1) +
      # adjust title based on input
      ggtitle(sprintf("%s Players Points Per Game", input$teamInput)) +
      # manipulates x-axis data so show much cleaner
      theme(axis.text.x = element_text(angle = 75, hjust = 1, size=7)))
  })
}

# run app
shinyApp(ui=ui, server=server)

