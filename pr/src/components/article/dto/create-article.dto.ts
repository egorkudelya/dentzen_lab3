import { IsDateString, IsInt, IsString, MaxLength } from 'class-validator';

export class CreateArticleDto {
  @IsString()
  @MaxLength(128)
  title: string;

  @IsString()
  text: string;

  @IsInt()
  views: number;

  @IsDateString()
  createdAt: string;

  @IsString()
  platformName: string;

  @IsInt()
  managerId: number;
}
