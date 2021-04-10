import random


class Trump:
    mark = None
    display_number = None
    numbers = None

    def __init__(self, mark, display_number, numbers):
        self.mark = mark
        self.display_number = display_number
        self.numbers = numbers

    def tostr(self):
        return self.mark + str(self.display_number)

    def get_numbers(self):
        return self.numbers


class Person:
    dealer = False
    name = ''
    trumps = []

    def __init__(self, dealer, name, trumps):
        self.dealer = dealer
        self.name = name
        self.trumps = trumps

    def get_trumps(self):
        return self.trumps


class BJ:
    trumps = []
    dealer = None
    persons = None

    def __init__(self):
        self.trumps = self.create_trumps()
        self.dealer = Person(
            True, 'Dealer', [self.trumps.pop(), self.trumps.pop()])
        self.persons = []

    def trump_numbers(self, num):
        if num == 1:
            return [1, 11]
        elif num > 1 and num < 10:
            return num
        else:
            return 10

    def create_trumps(self):
        trumps = []
        marks = ['♡', '♦', '♠', '♧']
        for num in range(0, 13):
            for mark in marks:
                trump = Trump(mark, num+1, self.trump_numbers(num+1))
                trumps.append(trump)
        random.shuffle(trumps)
        return trumps

    def display(self, person, hidden):
        print('--------')
        print(f'user_name:{person.name}')
        print(f'trumps:{self.display_trumps(person.get_trumps(), hidden)}')
        print('--------')

    def display_trumps(self, trumps, hidden):
        return ['Hidden' if hidden and i == 1 else x.tostr() for i, x in enumerate(trumps)]

    def add_person(self, name):
        person = Person(False, name, [self.trumps.pop(), self.trumps.pop()])
        self.persons.append(person)

    def get_persons(self):
        return self.persons

    def hit(self):
        return self.trumps.pop()

    def bj_calc(self, trumps):
        count = 0
        zan = []
        for trump in trumps:
            if isinstance(trump.get_numbers(), int):
                count += trump.get_numbers()
            else:
                # A
                zan.append(trump.get_numbers())

        for i, ace in enumerate(zan):
            if count + ace[1] > 21:
                count += ace[0]
            else:
                if i+1 != len(zan):
                    count += ace[0]
                else:
                    count += ace[1]
        return count

    def player_phase(self, person):
        while True:
            self.display(person, False)
            print('操作を選択してください（1:stand, 2:hit）：')
            try:
                num = int(input())
                if num == 1:
                    break
                elif num == 2:
                    person.get_trumps().append(self.hit())
            except Exception as e:
                print('入力可能な値を入力してください（1:stand, 2:hit）')
            calc = self.bj_calc(person.get_trumps())
            if calc > 21:
                self.display(person, False)
                print('21 を超えたのでターンを終了します')
                break

    def dealer_phase(self):
        count = 0
        sum = 0
        for person in self.persons:
            calc = self.bj_calc(person.get_trumps())
            if calc <= 21:
                sum += calc
                count += 1
        avg = 0
        if count > 0:
            avg = int(sum/count)

        self.display(self.dealer, False)

        dc = self.bj_calc(self.dealer.get_trumps())
        while True:
            if dc < 17 or dc < avg:
                self.dealer.get_trumps().append(self.hit())
                self.display(self.dealer, False)
                dc = self.bj_calc(self.dealer.get_trumps())
            elif dc == 21:
                break
            else:
                break

    def judge(self):
        # ディーラーの結果
        self.display(self.dealer, False)
        dc = self.bj_calc(self.dealer.get_trumps())
        if dc == 21:
            print('ブラックジャックでディーラーの勝利')
            return
        else:
            print(f'ディーラーの結果：{dc}点')

        for person in self.persons:
            calc = self.bj_calc(person.get_trumps())
            self.display(person, False)
            if calc == 21:
                print('ブラックジャックで勝利')
            elif calc < 21:
                if dc > 21:
                    print(f'{calc} 点で勝利')
                elif calc > dc:
                    print(f'{calc} 点で勝利')
                else:
                    print(f'{calc} 点で敗北')
            else:
                print(f'{calc} 点で敗北')


def main():

    print('何人で遊びますか？:')
    person = int(input())

    bj = BJ()

    for i in range(person):
        print(f'{i+1}人目の名前を入力してください:')
        name = input()
        bj.add_person(name)

    # ディーラー手札公開
    bj.display(bj.dealer, True)

    # ゲームフェーズ
    for person in bj.get_persons():
        bj.player_phase(person)

    print('プレイヤーフェーズが終了しました（Enter）')
    input()

    # ディーラーフェーズ
    bj.dealer_phase()
    print('ディーラーフェーズが終了しました（Enter）')
    input()

    # ジャッジフェーズ
    bj.judge()

    print('もう一度遊びますか？（y/n）')
    answer = input()
    if answer == 'y':
        main()


if __name__ == "__main__":
    main()
