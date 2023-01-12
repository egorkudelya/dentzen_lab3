import { Neo4jService } from 'nest-neo4j';

export const extractIsUpdatedFromQueryRes = (
  queryRes: Awaited<ReturnType<Neo4jService['write']>>,
) => queryRes.summary.counters.containsUpdates();
