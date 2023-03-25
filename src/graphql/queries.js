/* eslint-disable */
// this is an auto generated file. This will be overwritten

export const getMessages = /* GraphQL */ `
  query GetMessages($id: ID!) {
    getMessages(id: $id) {
      id
      lineUserId
      content
      role
      createdAt
      updatedAt
    }
  }
`;
export const listMessages = /* GraphQL */ `
  query ListMessages(
    $filter: ModelMessagesFilterInput
    $limit: Int
    $nextToken: String
  ) {
    listMessages(filter: $filter, limit: $limit, nextToken: $nextToken) {
      items {
        id
        lineUserId
        content
        role
        createdAt
        updatedAt
      }
      nextToken
    }
  }
`;
export const messagesByLineUserIdAndCreatedAt = /* GraphQL */ `
  query MessagesByLineUserIdAndCreatedAt(
    $lineUserId: String!
    $createdAt: ModelStringKeyConditionInput
    $sortDirection: ModelSortDirection
    $filter: ModelMessagesFilterInput
    $limit: Int
    $nextToken: String
  ) {
    messagesByLineUserIdAndCreatedAt(
      lineUserId: $lineUserId
      createdAt: $createdAt
      sortDirection: $sortDirection
      filter: $filter
      limit: $limit
      nextToken: $nextToken
    ) {
      items {
        id
        lineUserId
        content
        role
        createdAt
        updatedAt
      }
      nextToken
    }
  }
`;
