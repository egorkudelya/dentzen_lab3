export const makeCreateQuery = (tag: string, data: object) => {
  return `CREATE (n:${tag} {${Object.keys(data)
    .map((k) => `${k}:$${k}`)
    .join(',')}}) RETURN n`;
};
