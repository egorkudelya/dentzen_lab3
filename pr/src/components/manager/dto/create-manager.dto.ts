import { IsString } from 'class-validator';

export class CreateManagerDto {
  @IsString()
  name: string;
}
