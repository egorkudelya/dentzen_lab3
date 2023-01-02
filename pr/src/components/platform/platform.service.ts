import { Injectable, NotFoundException } from '@nestjs/common';
import { Neo4jService } from 'nest-neo4j';
import { extractDataFromQueryRes } from 'src/common/extractDataFromQueryRes';
import { extractIsUpdatedFromQueryRes } from 'src/common/extractIsUpdatedFromQueryRes';
import { makeCreateQuery } from 'src/common/makeCreateQuery';
import { makeUpdateQuery } from 'src/common/makeUpdateQuery';
import { CreatePlatformDto } from './dto/create-platform.dto';
import { UpdatePlatformDto } from './dto/update-platform.dto';

@Injectable()
export class PlatformService {
  constructor(private neo4jService: Neo4jService) {}

  async create(createPlatformDto: CreatePlatformDto) {
    return this.neo4jService
      .write(makeCreateQuery('Platform', createPlatformDto), createPlatformDto)
      .then(extractDataFromQueryRes({ one: true }));
  }

  async findAll() {
    return this.neo4jService
      .read('MATCH (p:Platform) RETURN p')
      .then(extractDataFromQueryRes());
  }

  async findOne(id: number) {
    return this.neo4jService
      .read('MATCH (p:Platform) WHERE ID(p) = $id RETURN p', { id })
      .then(extractDataFromQueryRes({ one: true }))
      .then((found) => {
        if (!found) {
          throw new NotFoundException(`No platform with id ${id} was found`);
        }

        return found;
      });
  }

  async update(id: number, updatePlatformDto: UpdatePlatformDto) {
    return this.neo4jService
      .write(makeUpdateQuery('Platform', updatePlatformDto), {
        id,
        ...updatePlatformDto,
      })
      .then((res) => {
        if (!extractIsUpdatedFromQueryRes(res)) {
          throw new NotFoundException(`No platform with id ${id} was found`);
        }

        return extractDataFromQueryRes({ one: true })(res);
      });
  }

  async remove(id: number) {
    return this.neo4jService
      .write('MATCH (p:Platform), (p)-[r]-() WHERE ID(p) = $id DELETE p, r', {
        id,
      })
      .then(extractIsUpdatedFromQueryRes)
      .then((deleted) => {
        if (!deleted) {
          throw new NotFoundException(`No platform with id ${id} was found`);
        }
      });
  }
}
