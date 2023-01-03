import { Injectable, NotFoundException } from '@nestjs/common';
import { Neo4jService } from 'nest-neo4j';
import { extractDataFromQueryRes } from 'src/common/extractDataFromQueryRes';
import { extractIsUpdatedFromQueryRes } from 'src/common/extractIsUpdatedFromQueryRes';
import { makeCreateQuery } from 'src/common/makeCreateQuery';
import { makeUpdateQuery } from 'src/common/makeUpdateQuery';
import { CreateArticleDto } from './dto/create-article.dto';
import { UpdateArticleDto } from './dto/update-article.dto';

@Injectable()
export class ArticleService {
  constructor(private neo4jService: Neo4jService) {}

  async create(createArticleDto: CreateArticleDto) {
    const { platformName, managerId, ...data } = createArticleDto;

    const article = await this.neo4jService
      .write(makeCreateQuery('Article', data), data)
      .then(extractDataFromQueryRes({ one: true }));

    await this.neo4jService
      .write(
        'MATCH (p:Platform { name: $platformName }), (a:Article) WHERE ID(a) = $articleId CREATE (a)-[:postedOn]->(p)',
        { platformName, articleId: +article.id },
      )
      .then(extractIsUpdatedFromQueryRes)
      .then((updated) => {
        if (!updated) {
          throw new NotFoundException(
            `No platform with name ${platformName} was found`,
          );
        }
      });

    await this.neo4jService
      .write(
        'MATCH (m:Manager), (a:Article) WHERE ID(a) = $articleId AND ID(m) = $managerId CREATE (a)-[:postedBy]->(m)',
        { managerId, articleId: +article.id },
      )
      .then(extractIsUpdatedFromQueryRes)
      .then((updated) => {
        if (!updated) {
          throw new NotFoundException(
            `No manager with id ${managerId} was found`,
          );
        }
      });

    return article;
  }

  findAll() {
    return this.neo4jService
      .read('MATCH (c:Article) RETURN c')
      .then(extractDataFromQueryRes());
  }

  findOne(id: number) {
    return this.neo4jService
      .read('MATCH (a:Article) WHERE ID(a) = $id RETURN a', { id })
      .then(extractDataFromQueryRes({ one: true }))
      .then((found) => {
        if (!found) {
          throw new NotFoundException(`No customer with id ${id} was found`);
        }

        return found;
      });
  }

  async update(id: number, updateArticleDto: UpdateArticleDto) {
    return this.neo4jService
      .write(makeUpdateQuery('Article', updateArticleDto), {
        id,
        ...updateArticleDto,
      })
      .then((res) => {
        if (!extractIsUpdatedFromQueryRes(res)) {
          throw new NotFoundException(`No Article with id ${id} was found`);
        }

        return extractDataFromQueryRes({ one: true })(res);
      });
  }

  async remove(id: number) {
    return this.neo4jService
      .write('MATCH (a:Article) WHERE ID(c) = $id DETACH DELETE a', {
        id,
      })
      .then(extractIsUpdatedFromQueryRes)
      .then((deleted) => {
        if (!deleted) {
          throw new NotFoundException(`No article with id ${id} was found`);
        }
      });
  }
}
