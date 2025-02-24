import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import timedelta

class QuickPlot:
    def __init__(self, dataframes, labels=None):
        self.dataframes = dataframes
        self.labels = labels if labels else [f"Series {i+1}" for i in range(len(dataframes))]
        self._validate_input()

    def _validate_input(self):
        if not isinstance(self.dataframes, list) or not all(isinstance(df, pd.DataFrame) for df in self.dataframes):
            raise ValueError("dataframes should be a list of pandas DataFrames.")
        if not all(len(df.columns) >= 2 for df in self.dataframes):
            raise ValueError("Each DataFrame should contain at least two columns.")
        if len(self.labels) != len(self.dataframes):
            raise ValueError("The number of labels should match the number of dataframes.")

    def plot_line(self, title="Line Plot", x='date', y='value', **layout_kwargs):
        fig = go.Figure()
        for df, label in zip(self.dataframes, self.labels):
            fig.add_trace(go.Scatter(x=df[x], y=df[y], mode='lines+markers+text', name=label, text=df[y]))

        fig.update_layout(title=title, xaxis_title=x, yaxis_title=y, **layout_kwargs)
        fig.update_xaxes(rangeslider=dict(visible=True), showgrid=False, tickformat='%b %Y')
        fig.update_yaxes(showgrid=False)
        fig.update_traces(textposition='top center')
        return fig

    def plot_bar(self, title="Bar Plot", x='date', y='value', **layout_kwargs):
        fig = go.Figure()
        for df, label in zip(self.dataframes, self.labels):
            fig.add_trace(go.Bar(x=df[x], y=df[y], name=label))
        fig.update_layout(title=title, xaxis_title=x, yaxis_title=y, **layout_kwargs)
        return fig

    def plot_scatter(self, title="Scatter Plot", x='date', y='value', **layout_kwargs):
        fig = go.Figure()
        for df, label in zip(self.dataframes, self.labels):
            fig.add_trace(go.Scatter(x=df[x], y=df[y], mode='markers', name=label))
        fig.update_layout(title=title, xaxis_title=x, yaxis_title=y, **layout_kwargs)
        return fig

    def prepare_figure(self, df, title):
        # Ensure 'date' is the index and convert to datetime
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)

        # Calculate latest rate and YoY changes
        latest_rate = df['value'].iloc[-1]
        yoy_change = df['value'].pct_change(12).iloc[-1]  # change from one year ago
        section_1 = f"Latest Refresh On: {df.index[-1].strftime('%a %b %d, %Y')}<br><b>{title}:</b> {latest_rate:,.2f} \
                <br><b>YoY Change:</b> {yoy_change:,.2f} bps"

        # Calculate Mean, Median, Min, and Max
        mean_val = df['value'].mean()
        median_val = df['value'].median()
        min_val = df['value'].min()
        min_date = df['value'].idxmin().strftime('%b %Y')
        max_val = df['value'].max()
        max_date = df['value'].idxmax().strftime('%b %Y')
        section_2 = f"<b>Mean:</b> {mean_val:,.2f}<br>" \
                    f"<b>Median:</b> {median_val:,.2f}<br><b>Min:</b> {min_val:,.2f} ({min_date})<br>" \
                    f"<b>Max:</b> {max_val:,.2f} ({max_date})"

        fig = go.Figure()

        # Add a line plot with a customized hover text and line style
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['value'],
            mode='lines',
            name=title,  # This is the right panel line name, for this case I do not want to show
            line=dict(color='darkblue', width=2),
            hovertemplate='Date: %{x}<br>Value: %{y:,.2f}'
        ))

        # Add low and high points for each year
        for year in df.index.year.unique():
            df_year = df[df.index.year == year]
            if not df_year.empty:
                min_idx = df_year['value'].idxmin()
                max_idx = df_year['value'].idxmax()

                # Low point use Red dot
                fig.add_trace(go.Scatter(
                    x=[min_idx],
                    y=[df_year['value'][min_idx]],
                    mode='markers',
                    name='Calendar Year Low' if year == df.index.year.unique()[-1] else None,  # Only label the last year
                    marker=dict(color='red'),
                    showlegend=False
                ))
                fig.add_annotation(
                    x=min_idx,
                    y=df_year['value'][min_idx],
                    text=f'{year} Low',
                    showarrow=True,
                    font=dict(color="black", size=12),
                    align="center",
                    arrowhead=2,
                    arrowsize=1,
                    arrowwidth=2,
                    arrowcolor="#636363",
                    ax=20,
                    ay=-30,
                    bordercolor="#c7c7c7",
                    borderwidth=2,
                    borderpad=4,
                    bgcolor="red",
                    opacity=0.8
                )

                # High point use Green Dot
                fig.add_trace(go.Scatter(
                    x=[max_idx],
                    y=[df_year['value'][max_idx]],
                    mode='markers',
                    name='Calendar Year High' if year == df.index.year.unique()[-1] else None,  # Only label the last year
                    marker=dict(color='green'),
                    showlegend=False
                ))
                fig.add_annotation(
                    x=max_idx,
                    y=df_year['value'][max_idx],
                    text=f'{year} High',
                    showarrow=True,
                    font=dict(color="black", size=12),
                    align="center",
                    arrowhead=2,
                    arrowsize=1,
                    arrowwidth=2,
                    arrowcolor="#636363",
                    ax=20,
                    ay=-30,
                    bordercolor="#c7c7c7",
                    borderwidth=2,
                    borderpad=4,
                    bgcolor="green",
                    opacity=0.8
                )

        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Value",
            plot_bgcolor='rgba(0, 0, 0, 0)',  # Transparent background
            xaxis=dict(
                showgrid=True,  # Show a grid
                gridcolor='rgba(200, 200, 200, 0.2)',  # Light grey grid lines
            ),
            yaxis=dict(
                showgrid=True,  # Show a grid
                gridcolor='rgba(200, 200, 200, 0.2)',  # Light grey grid lines
            ),
            legend=dict(  # This is used to position the line name/notes
                x=0.5,  # Horizontally centered
                y=-0.13,  # Position the legend below the plot
                xanchor='center',  # Anchor the legend at its center
            ),
            annotations=[  # This is for the setting within the text box
                dict(
                    x=df.index[1],  # Adjust where to locate text box
                    y=1,  # Text box vertical location
                    xref='x',
                    yref='paper',
                    text=section_1 + "<br><br>" + section_2,
                    showarrow=False,
                    align="left",  # Align text box content to left
                    xanchor='left',  # Adjust if left or right of the text box start point based on x-axis point
                    font=dict(size=12),
                    bgcolor="rgba(255, 255, 255, 1)",  # White background with full opacity
                )
            ]
        )
        return fig

# Example usage
if __name__ == "__main__":
    # Sample data for demonstration
    data = {
        'date': pd.date_range(start='1/1/2020', periods=100),
        'value': range(100)
    }
    df = pd.DataFrame(data)

    # Initialize QuickPlot with dataframes
    qp = QuickPlot(dataframes=[df], labels=["Sample Data"])

    # Plot line, bar, scatter charts
    fig_line = qp.plot_line(title="Sample Line Plot")
    fig_bar = qp.plot_bar(title="Sample Bar Plot")
    fig_scatter = qp.plot_scatter(title="Sample Scatter Plot")

    fig_line.show()
    fig_bar.show()
    fig_scatter.show()

    # Prepare a specific figure similar to the plotter.py example
    fig_custom = qp.prepare_figure(df, title="Sample Custom Plot")
    fig_custom.show()
