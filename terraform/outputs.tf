output "lambda_function_url" {
  description = "Lambda Function URL（トラッキングピクセルのエンドポイント）"
  value       = aws_lambda_function_url.tracker.function_url
}

output "lambda_function_name" {
  description = "Lambda関数名"
  value       = aws_lambda_function.tracker.function_name
}

output "cloudwatch_log_group" {
  description = "CloudWatch Logsのロググループ名"
  value       = aws_cloudwatch_log_group.tracker.name
}
