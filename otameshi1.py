import datetime
import json 

class Kakeibo:
    # データをjsonファイルに保存するメソッド
    def save_data(self):
        data = {
            'expense_year': self.expense_year,
            'expense_month': self.expense_month,
            'expense_week': self.expense_week,
            'expense_day': self.expense_day,
            'last_update': self.last_update.isoformat()
        }
        with open('kakeibo_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    def __init__(self):
        self.expense_year = 0
        self.expense_month = 0
        self.expense_week = 0
        self.expense_day = 0
        self.last_update = datetime.datetime.now() # 最後に更新した日時を記録
        # ファイルからデータを読み込み、各変数に上書きする処理
        try:
            with open('kakeibo_data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.expense_year = data.get('expense_year', 0)
                self.expense_month = data.get('expense_month', 0)
                self.expense_week = data.get('expense_week', 0)
                self.expense_day = data.get('expense_day', 0)
                last_update_str = data.get('last_update')
                if last_update_str:
                    self.last_update = datetime.datetime.fromisoformat(last_update_str)
        except (FileNotFoundError, json.JSONDecodeError, ValueError):
            # ファイルがない場合やデータが不正な場合は初期値のまま
            pass

    # 日付が変わったかどうかをチェックし、必要なら繰り越し処理を行うメソッド
    def check_rollover(self):
        now = datetime.datetime.now()
        previous = self.last_update
        if now.year > previous.year:
            self.expense_year = 0
            self.expense_month = 0
            self.expense_week = 0
            self.expense_day = 0
            # 年が変わったら全てリセット
        elif now.month > previous.month:
            # 月が変わったら...
            self.expense_month = 0
        elif now.weekday() < previous.weekday() or (now.day - previous.day) >= 7:
            # 週の始まりが月曜日なので、週が変わったら...
            self.expense_week = 0
        elif now.day > previous.day:
            # 日が変わったら...
            self.expense_day = 0
        
        # 2. 全てのチェックが終わったら、最後に「最終更新日時」を現在時刻に更新する
        self.last_update = now

    # 支出を追加するためのメソッド
    def add_expense(self, amount):
        # 3. 支出を追加する「前」に、必ず日付の繰り越しチェックを行う
        self.check_rollover()

        # 4. 渡されたamountを、日・週・月の支出に加算する
        self.expense_day += int(amount)
        self.expense_week += int(amount)
        self.expense_month += int(amount)
        self.expense_year += int(amount)

        print(f"今年の支出: {self.expense_year}円")
        print(f"今月の支出: {self.expense_month}円")
        print(f"今週の支出: {self.expense_week}円")
        print(f"今日の支出: {self.expense_day}円")
        # 5. 最後に、データをファイルに保存する
        self.save_data()


# --- 使い方のイメージ ---
#
def main():
    # 1. 記録されたデータの読み込み（Kakeiboの__init__で自動）
    kakeibo = Kakeibo()
    # 2. 日付チェックと必要な修正操作
    kakeibo.check_rollover()
    # 3. 家計簿アプリの開始画面（現在時刻、現在までの支出状況の表示）
    now = datetime.datetime.now()
    print("家計簿アプリを起動しました！")
    print(f"現在の日時: {now.year}年{now.month}月{now.day}日")
    print(f"今年の支出: {kakeibo.expense_year}円")
    print(f"今月の支出: {kakeibo.expense_month}円")
    print(f"今週の支出: {kakeibo.expense_week}円")
    print(f"今日の支出: {kakeibo.expense_day}円")

    # 4. 支出の記録開始画面
    while True:
        print("\n--- メニュー ---")
        print("1. 支出を記録する")
        print("2. 終了")
        choice = input("選択してください: ")
        if choice == "2":
            print("家計簿アプリを終了します。")
            break
        elif choice == "1":
            try:
                amount = int(input("いくら使用しましたか？: "))
                kakeibo.add_expense(amount)
            except ValueError:
                print("数値で入力してください。")
        else:
            print("無効な選択です。もう一度選んでください。")

if __name__ == "__main__":
    main()
#     # ... whileループの中で ...
#     # my_kakeibo.add_expense(expense_amount) のように呼び出す