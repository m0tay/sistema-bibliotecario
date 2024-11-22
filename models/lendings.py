import pandas as pd

def calculate_loan_schedule(principal, annual_rate, years, payments_per_year=12):
    """
    Calcula o cronograma de amortização de um empréstimo.
    
    Args:
        principal (float): Valor principal do empréstimo.
        annual_rate (float): Taxa de juros anual (em decimal, por exemplo, 0.05 para 5%).
        years (int): Duração do empréstimo em anos.
        payments_per_year (int): Número de pagamentos por ano (padrão é 12).
    
    Returns:
        DataFrame: Tabela com detalhes do cronograma de pagamento.
    """
    # Taxa de juros mensal
    monthly_rate = annual_rate / payments_per_year
    
    # Número total de pagamentos
    total_payments = years * payments_per_year
    
    # Fórmula para o pagamento mensal fixo
    monthly_payment = principal * (monthly_rate * (1 + monthly_rate) ** total_payments) / \
                      ((1 + monthly_rate) ** total_payments - 1)
    
    # Variáveis para armazenar os dados do cronograma
    balance = principal
    schedule = []

    for i in range(1, total_payments + 1):
        # Cálculo dos juros do mês
        interest = balance * monthly_rate
        # Pagamento do principal
        principal_payment = monthly_payment - interest
        # Atualizar o saldo
        balance -= principal_payment
        
        # Evitar saldo negativo devido a arredondamentos
        balance = max(balance, 0)
        
        # Adicionar ao cronograma
        schedule.append({
            "Payment #": i,
            "Monthly Payment": round(monthly_payment, 2),
            "Interest Paid": round(interest, 2),
            "Principal Paid": round(principal_payment, 2),
            "Remaining Balance": round(balance, 2)
        })

    # Retornar o cronograma como um DataFrame
    return pd.DataFrame(schedule)


# Exemplo de uso:
principal = 100  # Valor do empréstimo
annual_rate = 0.05  # Taxa de juros anual (5%)
years = 1  # Duração em anos

loan_schedule = calculate_loan_schedule(principal, annual_rate, years)

# Mostrar os primeiros registros do cronograma
import ace_tools as tools; tools.display_dataframe_to_user(name="Cronograma de Pagamento de Empréstimo", dataframe=loan_schedule)
