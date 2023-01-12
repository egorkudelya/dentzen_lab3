import { Injectable, NotFoundException } from '@nestjs/common';
import { Neo4jService } from 'nest-neo4j';
import { extractDataFromQueryRes } from 'src/common/extractDataFromQueryRes';
import { extractIsUpdatedFromQueryRes } from 'src/common/extractIsUpdatedFromQueryRes';
import { makeCreateQuery } from 'src/common/makeCreateQuery';
import { makeUpdateQuery } from 'src/common/makeUpdateQuery';
import { CreateCustomerDto } from './dto/create-customer.dto';
import { RateArticleDto } from './dto/rate-article.dto';
import { UpdateCustomerDto } from './dto/update-customer.dto';

@Injectable()
export class CustomerService {
  constructor(private neo4jService: Neo4jService) {}

  async create(createCustomerDto: CreateCustomerDto) {
    const { cameFromPlatform, ...data } = createCustomerDto;

    const customer = await this.neo4jService
      .write(makeCreateQuery('Customer', data), data)
      .then(extractDataFromQueryRes({ one: true }));

    await this.neo4jService
      .write(
        'MATCH (p:Platform { name: $platformName }), (c:Customer) WHERE ID(c) = $customerId CREATE (c)-[:cameFrom]->(p)',
        { platformName: cameFromPlatform, customerId: +customer.id },
      )
      .then(extractIsUpdatedFromQueryRes)
      .then((updated) => {
        if (!updated) {
          throw new NotFoundException(
            `No platform with name ${cameFromPlatform} was found`,
          );
        }
      });

    return customer;
  }

  async rateArticle(id: number, rateArticleDto: RateArticleDto) {
    await this.neo4jService
      .write(
        'MATCH (a:Article), (c:Customer) WHERE ID(c) = $customerId AND ID(a) = $articleId CREATE (c)-[:rated { rating: $rating }]->(a)',
        { customerId: id, ...rateArticleDto },
      )
      .then(extractIsUpdatedFromQueryRes)
      .then((updated) => {
        if (!updated) {
          throw new NotFoundException(`No article or customer were found`);
        }
      });
  }

  async findAll() {
    return this.neo4jService
      .read('MATCH (c:Customer) RETURN c')
      .then(extractDataFromQueryRes());
  }

  async findOne(id: number) {
    return this.neo4jService
      .read('MATCH (p:Customer) WHERE ID(p) = $id RETURN p', { id })
      .then(extractDataFromQueryRes({ one: true }))
      .then((found) => {
        if (!found) {
          throw new NotFoundException(`No customer with id ${id} was found`);
        }

        return found;
      });
  }

  async update(id: number, updateCustomerDto: UpdateCustomerDto) {
    return this.neo4jService
      .write(makeUpdateQuery('Customer', updateCustomerDto), {
        id,
        ...updateCustomerDto,
      })
      .then((res) => {
        if (!extractIsUpdatedFromQueryRes(res)) {
          throw new NotFoundException(`No Customer with id ${id} was found`);
        }

        return extractDataFromQueryRes({ one: true })(res);
      });
  }

  async remove(id: number) {
    return this.neo4jService
      .write('MATCH (c:Customer) WHERE ID(c) = $id DETACH DELETE c', {
        id,
      })
      .then(extractIsUpdatedFromQueryRes)
      .then((deleted) => {
        if (!deleted) {
          throw new NotFoundException(`No customer with id ${id} was found`);
        }
      });
  }
}
