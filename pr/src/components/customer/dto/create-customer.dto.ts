import {
  IsDateString,
  IsEmail,
  IsEnum,
  IsPhoneNumber,
  IsString,
} from 'class-validator';

export class CreateCustomerDto {
  @IsDateString()
  birthday: string;

  @IsEnum(['male', 'female'])
  gender: string;

  @IsString()
  name: string;

  @IsEmail()
  email: string;

  @IsPhoneNumber()
  phone: string;

  @IsString()
  location: string;

  @IsString()
  cameFromPlatform: string;
}
