// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Aggregator {

    // Structure to represent a request
    struct Request {
        string message;
        address requester;
        bool served;
    }

    // Mapping to store requests by an integer identifier
    mapping(uint256 => Request) public requests;
    // Counter for unique request identifiers
    uint256 private requestCount;

    // Event declaration
    event RequestCreated(uint256 indexed requestId, string indexed message);

    // Method to create a new request
    function newRequest(string memory message) public returns (uint256) {
        requestCount++;

        // Create a new request
        requests[requestCount] = Request({
            message: message,
            requester: msg.sender,
            served: false
        });

        // Emit the RequestCreated event
        emit RequestCreated(requestCount, message);
        
        // Return the unique identifier of the created request
        return requestCount;
    }

    // Returns the status of a request.
    function getRequestStatus(uint256 requestId) public view returns (bool) {
        Request memory req = requests[requestId];
        return req.served;
    }

    // Returns the number of created requests.
    function getRequestCount() public view returns (uint256) {
        return requestCount;
    }

}
