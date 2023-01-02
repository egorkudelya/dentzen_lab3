import { Injectable, NotFoundException } from '@nestjs/common';
import { Neo4jService } from 'nest-neo4j';
import { extractDataFromQueryRes } from 'src/common/extractDataFromQueryRes';
import { extractIsUpdatedFromQueryRes } from 'src/common/extractIsUpdatedFromQueryRes';
import { makeCreateQuery } from 'src/common/makeCreateQuery';
import { makeUpdateQuery } from 'src/common/makeUpdateQuery';
import { CreateManagerDto } from './dto/create-manager.dto';
import { UpdateManagerDto } from './dto/update-manager.dto';

@Injectable()
export class ManagerService {
  constructor(private neo4jService: Neo4jService) {}

  create(createManagerDto: CreateManagerDto) {
    return this.neo4jService
      .write(makeCreateQuery('Manager', createManagerDto), createManagerDto)
      .then(extractDataFromQueryRes({ one: true }));
  }

  findAll() {
    return this.neo4jService
      .read('MATCH (m:Manager) RETURN m')
      .then(extractDataFromQueryRes());
  }

  findOne(id: number) {
    return this.neo4jService
      .read('MATCH (m:Manager) WHERE ID(p) = $id RETURN p', { id })
      .then(extractDataFromQueryRes({ one: true }))
      .then((found) => {
        if (!found) {
          throw new NotFoundException(`No customer with id ${id} was found`);
        }

        return found;
      });
  }

  update(id: number, updateManagerDto: UpdateManagerDto) {
    return this.neo4jService
      .write(makeUpdateQuery('Manager', updateManagerDto), {
        id,
        ...updateManagerDto,
      })
      .then((res) => {
        if (!extractIsUpdatedFromQueryRes(res)) {
          throw new NotFoundException(`No manager with id ${id} was found`);
        }

        return extractDataFromQueryRes({ one: true })(res);
      });
  }

  remove(id: number) {
    return this.neo4jService
      .write('MATCH (m:Manager), (c)-[r]-() WHERE ID(c) = $id DELETE m, r', {
        id,
      })
      .then(extractIsUpdatedFromQueryRes)
      .then((deleted) => {
        if (!deleted) {
          throw new NotFoundException(`No manager with id ${id} was found`);
        }
      });
  }
}
