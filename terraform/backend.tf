terraform {
  backend "s3" {
    bucket         = "milo87-terraform-states"
    key            = "dhcalc.tfstate"
    region         = "eu-west-2"
    dynamodb_table = "TerraformLock"
  }
}