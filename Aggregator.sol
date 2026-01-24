// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Aggregator {

    // Struct to hold request details
    struct Request {
        string message;
        address requester;
        bool served;
    }

    // Mapping from request ID to Request struct
    mapping(uint256 => Request) public requests;

    // Tracks the total number of requests
    uint256 private requestCount;

    // Triggered when a new request is created
    event RequestCreated(uint256 indexed requestId, address indexed requester, bytes32 messageHash);

    // Triggered when a request is served
    event RequestServed(uint256 indexed requestId);

    // Creates a new request and returns its ID
    function newRequest(string calldata message) external returns (uint256) {
        requestCount++;

        requests[requestCount] = Request({
            message: message,
            requester: msg.sender,
            served: false
        });

        bytes32 messageHash = keccak256(abi.encodePacked(message));

        emit RequestCreated(requestCount, msg.sender, messageHash);

        return requestCount;
    }

    // Serves a request by its ID
    // TODO: Implement access control to restrict who can serve requests
    function serveRequest(uint256 requestId) external {
        require(requestId > 0 && requestId <= requestCount, "Invalid request");
        require(!requests[requestId].served, "Already served");

        requests[requestId].served = true;
        emit RequestServed(requestId);
    }

    // Retrieves the status of a request by its ID
    // TODO: Implement access control to restrict who can view request status
    function getRequestStatus(uint256 requestId) external view returns (bool) {
        require(requestId > 0 && requestId <= requestCount, "Invalid request");
        return requests[requestId].served;
    }

    // Retrieves the total number of requests
    function getRequestCount() external view returns (uint256) {
        return requestCount;
    }
}
