##################################################
# ECR
##################################################

resource "aws_ecr_repository" "dhcalc" {
  name                 = "dhcalc"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

data "aws_iam_policy_document" "dhcalc_access" {
  statement {
    effect = "Allow"

    principals {
      type        = "AWS"
      identifiers = [aws_lightsail_container_service.dhcalc.private_registry_access[0].ecr_image_puller_role[0].principal_arn]
    }

    actions = [
      "ecr:BatchGetImage",
      "ecr:GetDownloadUrlForLayer",
    ]
  }
}

resource "aws_ecr_repository_policy" "dhcalc" {
  repository = aws_ecr_repository.dhcalc.name
  policy     = data.aws_iam_policy_document.dhcalc_access.json
}

##################################################
# Lightsail
##################################################

resource "aws_lightsail_container_service" "dhcalc" {
  name = "dh-combat-calculator"

  power = "nano"
  scale = 1

  private_registry_access {
    ecr_image_puller_role {
      is_active = true
    }
  }

  public_domain_names {
    certificate {
      certificate_name = "dh-gilbro-net"
      domain_names = [
        "dh.gilbro.net"
      ]
    }
  }
}

resource "aws_lightsail_container_service_deployment_version" "current" {
  container {
    container_name = "dhcalc"
    image          = "${aws_ecr_repository.dhcalc.repository_url}:v0.0.1"

    command = []

    ports = {
      5000 = "HTTP"
    }
  }

  public_endpoint {
    container_name = "dhcalc"
    container_port = 5000

    health_check {}
  }

  service_name = aws_lightsail_container_service.dhcalc.name
}

##################################################
# Certificate
##################################################

resource "aws_lightsail_certificate" "dh_gilbro_net" {
  name        = "dh-gilbro-net"
  domain_name = "dh.gilbro.net"
}

data "aws_route53_zone" "gilbro_net" {
  name = "gilbro.net"

  private_zone = false
}

resource "aws_route53_record" "dhcalc" {
  zone_id = data.aws_route53_zone.gilbro_net.zone_id

  name            = "dh"
  allow_overwrite = true
  type            = "CNAME"
  ttl             = 300

  records = [
    split("/", aws_lightsail_container_service.dhcalc.url)[2]
  ]
}