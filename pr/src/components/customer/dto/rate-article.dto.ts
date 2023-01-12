import { IsInt, Max, Min } from 'class-validator';

export class RateArticleDto {
  @IsInt()
  articleId: number;

  @IsInt()
  @Min(1)
  @Max(10)
  rating: number;
}
