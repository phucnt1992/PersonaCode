Feature: Get Markets from Spotify

    System can get markets data from Spotify

    Scenario: Get the markets data
        Given system has client credentials
        When I request to get market data
        Then the market data should be received
