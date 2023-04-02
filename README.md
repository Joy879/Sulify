# Sulify

A simple song recommender



![sulify](https://user-images.githubusercontent.com/70502261/189855922-73811df8-be1d-4e90-8f47-2e719e0b2d01.png)


### About the app :bulb:
A song recommender that takes in data from [Spotify API](https://developer.spotify.com/documentation/web-api/) and displays various aspects in a dashboard. 
I wanted to explore how recommender systems work and use Python based tools for development since its the go to language for most Data Science projects.

* View the webapp [here](https://sulify.onrender.com/)


### How it works :feet:

Sulify is a dash app. The structure is as follows:

```bash
- app.py
   |-- audio features
   |-- recommender
 ```
 
The audio features tab is meant to explore a single song's features.
A user searches for a song and selects the specific song and artist from the dropdowm menu and gets to see a preview of the song, audio features displayed as numbers and displayed as graphs.



The recommender tab is meant to make requests to a [model](https://suliapi.onrender.com/docs) hosted as an API. The response is a list of ten songs that the user can preview and also view a graph of similarity scores.


### Main libraries used: :books:

| Tool/Library                                                   | Purpose                      |
| -------------------------------------------------------------- | -----------------------------|
| [Dash](https://dash.plotly.com/)                               | Dashboard design  :grinning:           |
| [Dash Bootstrap Components](http://dash-bootstrap-components.opensource.faculty.ai/)            | Bring boostrap to dash apps             |
| [Plotly](https://plotly.com/python)                            | Interactive Graphs   :bar_chart:        |
| [spotipy](https://pypi.org/project/spotipy/)                       | Connect to Spotify    |
| [scikit-learn](https://scikit-learn.org/stable/index.html)                       | Get similarity scores and graph :chart_with_upwards_trend: |


### Main Feature :pushpin:
User searches for a song and either gets a summary of all audio features or a recommendation of similar songs all displayed in a visually pleasing manner. 

All this is made possible through Dash.
Dash has two main parts:
* Layout - the HTML and DCC components that design the static webpage
* Callbacks - Inputs and Outputs that define how the webpage becomes dynamic

### Installation :inbox_tray:

#### Prerequisites:

- [ ] A Spotify free account which will give you access to an API key

         
              git clone https://github.com/Joy879/Sulify
              pip install -r requirements.txt
 
### Licensing :lock:
This project is licensed under the MIT License - see the [LICENSE](https://github.com/Joy879/Sulify/blob/main/LICENSE) file for details.

### Future
I am looking forward to collecting more data to make the recommender model more accurate and faster. This project is my own way of exploring various strategies of  implementing content-based recommender systems. The accuracy vs speed tradeoff is definitely an issue i'd like to dive deeper into even as I learn how to optimize the app to work with larger datasets. I would also like to allow a user to login to spotify from the app and be able to save the recommended songs into a playlist.
If you have any ideas or suggestions or contributions feel free to reach out to me via [mail](joywanjiru879@gmail.com) :e-mail:


### Author :black_nib:
#### Joy Wanjiru

I am a data science enthusiast and a software engineering graduate from ALX and I love working with Python especially because of it's vast pool of libraries for scientific computing

