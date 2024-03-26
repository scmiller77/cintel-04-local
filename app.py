
import plotly.express as px
import seaborn as sns
from shiny.express import input, ui
from shiny import render, reactive, req
from shinywidgets import render_plotly, render_widget
import palmerpenguins

penguins = palmerpenguins.load_penguins()

ui.page_opts(title="Smiller's Penguin Report", fillable=True)


@reactive.calc
def filtered_data():
    # The required function req() is used to ensure that
    # the input.selected_species_list() function is not empty.
    req(input.selected_species_list())

    # If empty, req() will stop the execution and
    # we'll just wait until the associated input changes to not empty.
    # If not empty, we'll continue and filter the data.
    isSpeciesMatch = penguins["species"].isin(input.selected_species_list())

    return penguins[isSpeciesMatch]


with ui.sidebar(open="open"):
    # Add a second-level header to the sidebar
    ui.h2("Sidebar")

    ui.input_selectize(
        "selected_attribute",
        "Choose Attribute",
        ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"],
    )

    # Numeric input for the number of Plotly histogram bins
    ui.input_numeric("plotly_bin_count", "Histogram Bins", 25)

    # Slider input for the number of Seaborn bins
    ui.input_slider(
        "seaborn_bin_count", "Seaborn Bins", 1, 60, 30
    )  # Minimum, maximum, default values

    ui.input_checkbox_group(
        "selected_species_list",
        "Filter Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo"],
        inline=True,
    )  # Selected options and inline display

    # Add a horizontal rule
    ui.hr()

    # Add a hyperlink
    ui.a("GitHub", href="https://github.com/scmiller77", target="_blank")

with ui.layout_columns():
    with ui.card():

        @render.data_frame
        def penguins_df():
            return render.DataTable(penguins)

    with ui.card():

        @render.data_frame
        def penguins_dg():
            return render.DataGrid(penguins)


with ui.layout_columns():

    @render_widget
    def plot1():
        scatterplot = px.histogram(
            data_frame=filtered_data(),
            x=input.selected_attribute(),
            nbins=input.plotly_bin_count(),
            color="species",
        ).update_layout(
            title={"text": "Palmer Penguins - Plotly", "x": 0.5},
            yaxis_title="Value",
        )
        return scatterplot

    @render.plot(alt="A Seaborn histogram on penguin body mass in grams.")
    def plot2():
        ax = sns.histplot(
            data=filtered_data(),
            x=input.selected_attribute(),
            hue="species",
            bins=input.seaborn_bin_count(),
        )
        ax.set_title("Palmer Penguins - Seaborn")
        ax.set_ylabel("Value")
        return ax

    @render_plotly
    def plotly_scatterplot():
        return px.scatter(
            filtered_data(),
            x="bill_length_mm",
            y="body_mass_g",
            color="species",
            title="Palmer Penguins - Plotly Scatterplot",
            labels={
                "bill_length_mm": "Bill Length (mm)",
                "body_mass_g": "Body Mass (g)",
            },
            size_max=8,  # set the maximum marker size
        )
