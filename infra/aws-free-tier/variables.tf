variable "project_name" {
  type    = string
  default = "driftdock"
}

variable "suffix" {
  type        = string
  description = "Lowercase suffix to keep the bucket name unique"
}

variable "aws_region" {
  type    = string
  default = "us-east-1"
}
