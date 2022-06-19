Feature: Fetch Markets Command

    System can fetch avaialable markets from Spotify via "fetch_markets" command

    Scenario: Fetch markets command should be success
        Given system has client credentials
        When the user calls "fetch_markets" command
        Then the output should return successful message
        And the new markets should be stored in db


