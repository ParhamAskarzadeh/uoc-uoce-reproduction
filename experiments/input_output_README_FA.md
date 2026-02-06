# اجرای اسکریپت ورودی–خروجی (دموی CPU)

این اسکریپت یک دمو بسیار سبک است که بدون اجرای مدل واقعی، یک خروجی UOCE‌مانند تولید می‌کند.

## ورودی
- فایل CSV با یک ستون به نام `text`.
- نمونه آماده: `project/experiments/sample_input.csv`

## اجرا
```bash
python3 project/experiments/run_rule_based_inference.py \
  project/experiments/sample_input.csv \
  project/experiments/sample_output.csv
```

## خروجی
- فایل خروجی: `project/experiments/sample_output.csv`
- شامل ستون‌های UOCE:
  - `aspect_term`, `sentiment_expression`, `target_entity`, `aspect_category`,
    `sentiment_polarity`, `sentiment_intensity`, `opinion_holder_*`, `qualifier`, `reason`

## نکته
این خروجی فقط برای دمو و تست روی CPU است و جایگزین مدل واقعی نیست.
