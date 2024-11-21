from rest_framework import serializers

class ExchangeRateSerializer(serializers.Serializer):
    cur_unit = serializers.CharField()  # Currency code (e.g., USD)
    ttb = serializers.DecimalField(max_digits=10, decimal_places=2)  # Telegraphic Transfer Buying rate
    tts = serializers.DecimalField(max_digits=10, decimal_places=2)  # Telegraphic Transfer Selling rate
    deal_bas_r = serializers.DecimalField(max_digits=10, decimal_places=2)  # Basic exchange rate
    bkpr = serializers.DecimalField(max_digits=10, decimal_places=2)  # Book price
    yy_efee_r = serializers.DecimalField(max_digits=10, decimal_places=5)  # Annual exchange fee rate
    ten_dd_efee_r = serializers.DecimalField(max_digits=10, decimal_places=5)  # 10-day exchange fee rate
    kftc_bkpr = serializers.DecimalField(max_digits=10, decimal_places=2)  # KFTC book price
    kftc_deal_bas_r = serializers.DecimalField(max_digits=10, decimal_places=2)  # KFTC basic exchange rate
    cur_nm = serializers.CharField()  # Currency name (e.g., 미국 달러)