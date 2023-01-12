export const makeUpdateQuery = (tag: string, data: object) => {
  return `MATCH (n:${tag}) WHERE ID(n) = $id SET ${Object.keys(data)
    .map((key) => `n.${key} = $${key}`)
    .join(',')} RETURN n`;
};
