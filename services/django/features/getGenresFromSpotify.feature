Feature: Get Genres from Spotify

    System can get genres data from Spotify

    Scenario: Get the genres data
        Given system has client credentials
        When I request to get genre data
        Then the genre data should be received
