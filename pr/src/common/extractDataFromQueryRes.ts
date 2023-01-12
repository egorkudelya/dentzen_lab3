import { Neo4jService } from 'nest-neo4j';

export const extractDataFromQueryRes =
  ({ one }: { one?: boolean } = {}) =>
  (queryRes: Awaited<ReturnType<Neo4jService['read']>>) => {
    if (one) {
      const node = queryRes?.records[0]?.values()?.next()?.value;
      return node && { id: node['elementId'], ...node['properties'] };
    }

    return queryRes?.records?.flatMap((record) =>
      Array.from(record?.values() || []).map((node) => ({
        id: node['elementId'],
        ...node['properties'],
      })),
    );
  };
