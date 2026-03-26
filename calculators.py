import streamlit as st
import numpy as np
import plotly.graph_objects as go

def sip_calculator():
    """SIP (Systematic Investment Plan) Calculator"""
    st.subheader("📈 SIP Calculator")
    st.markdown("Calculate how much your monthly investments can grow")
    
    col1, col2 = st.columns(2)
    
    with col1:
        monthly_investment = st.number_input("Monthly Investment (₹)", min_value=500.0, value=5000.0, step=500.0, key="sip_monthly_input")
        years = st.number_input("Investment Period (Years)", min_value=1.0, max_value=30.0, value=10.0, step=1.0, key="sip_years_input")
    
    with col2:
        expected_return = st.number_input("Expected Return (%)", min_value=1.0, max_value=20.0, value=12.0, step=0.5, key="sip_return_input")
    
    # Calculate
    months = years * 12
    rate_per_month = expected_return / (12 * 100)
    
    # Future Value of SIP
    if rate_per_month > 0:
        future_value = monthly_investment * ((1 + rate_per_month) ** months - 1) / rate_per_month * (1 + rate_per_month)
    else:
        future_value = monthly_investment * months
    
    total_investment = monthly_investment * months
    
    # Display Results
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Investment", f"₹{total_investment:,.0f}")
    with col2:
        st.metric("Estimated Returns", f"₹{future_value - total_investment:,.0f}")
    with col3:
        st.metric("Total Value", f"₹{future_value:,.0f}")
    
    # Create chart
    years_list = list(range(1, int(years) + 1))
    yearly_values = []
    
    for year in years_list:
        months_done = year * 12
        if rate_per_month > 0:
            val = monthly_investment * ((1 + rate_per_month) ** months_done - 1) / rate_per_month * (1 + rate_per_month)
        else:
            val = monthly_investment * months_done
        yearly_values.append(val)
    
    fig = go.Figure(data=[
        go.Bar(name='Investment', x=years_list, y=[monthly_investment * 12 * i for i in years_list]),
        go.Bar(name='Returns', x=years_list, y=[val - (monthly_investment * 12 * i) for i, val in enumerate(yearly_values, 1)])
    ])
    
    fig.update_layout(barmode='stack', title="Year-wise Growth", xaxis_title="Years", yaxis_title="Amount (₹)")
    st.plotly_chart(fig, use_container_width=True)

def lumpsum_calculator():
    """Lumpsum Investment Calculator"""
    st.subheader("💰 Lumpsum Calculator")
    st.markdown("Calculate how your one-time investment grows")
    
    col1, col2 = st.columns(2)
    
    with col1:
        investment = st.number_input("Investment Amount (₹)", min_value=1000.0, value=100000.0, step=10000.0, key="lumpsum_amount_input")
        years = st.number_input("Investment Period (Years)", min_value=1.0, max_value=30.0, value=5.0, step=1.0, key="lumpsum_years_input")
    
    with col2:
        expected_return = st.number_input("Expected Return (%)", min_value=1.0, max_value=20.0, value=10.0, step=0.5, key="lumpsum_return_input")
    
    # Calculate
    future_value = investment * (1 + expected_return / 100) ** years
    
    # Display Results
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Initial Investment", f"₹{investment:,.0f}")
    with col2:
        st.metric("Total Returns", f"₹{future_value - investment:,.0f}")
    with col3:
        st.metric("Final Value", f"₹{future_value:,.0f}")
    
    # Create chart
    years_list = list(range(int(years) + 1))
    values = [investment * (1 + expected_return / 100) ** y for y in years_list]
    
    fig = go.Figure(data=go.Scatter(x=years_list, y=values, mode='lines+markers'))
    fig.update_layout(title="Growth Over Time", xaxis_title="Years", yaxis_title="Amount (₹)")
    st.plotly_chart(fig, use_container_width=True)

def emi_calculator():
    """Loan EMI Calculator"""
    st.subheader("🏠 Loan EMI Calculator")
    st.markdown("Calculate your monthly loan payments")
    
    col1, col2 = st.columns(2)
    
    with col1:
        loan_amount = st.number_input("Loan Amount (₹)", min_value=10000.0, value=500000.0, step=50000.0, key="emi_amount_input")
        years = st.number_input("Loan Tenure (Years)", min_value=1.0, max_value=30.0, value=20.0, step=1.0, key="emi_years_input")
    
    with col2:
        interest_rate = st.number_input("Interest Rate (%)", min_value=0.1, max_value=20.0, value=8.5, step=0.5, key="emi_rate_input")
    
    # Calculate EMI
    months = years * 12
    monthly_rate = interest_rate / (12 * 100)
    
    # EMI Formula: P * r * (1+r)^n / ((1+r)^n - 1)
    if monthly_rate > 0:
        emi = loan_amount * monthly_rate * (1 + monthly_rate) ** months / ((1 + monthly_rate) ** months - 1)
    else:
        emi = loan_amount / months
    
    total_payment = emi * months
    total_interest = total_payment - loan_amount
    
    # Display Results
    st.markdown("---")
    
    # Show results in a nice format
    result_col1, result_col2, result_col3 = st.columns(3)
    
    with result_col1:
        st.metric("Monthly EMI", f"₹{emi:,.0f}")
    with result_col2:
        st.metric("Total Interest Payable", f"₹{total_interest:,.0f}")
    with result_col3:
        st.metric("Total Payment", f"₹{total_payment:,.0f}")
    
    # Additional info
    st.markdown("---")
    st.info(f"📊 **Summary:** For a loan of ₹{loan_amount:,.0f} at {interest_rate}% for {int(years)} years, you'll pay ₹{emi:,.0f} every month.")
    
    # Create payment breakdown chart
    try:
        # Calculate yearly breakdown
        years_list = []
        principal_per_year = []
        interest_per_year = []
        
        remaining = loan_amount
        
        for year in range(1, int(years) + 1):
            yearly_principal = 0
            yearly_interest = 0
            
            for month in range(12):
                if remaining <= 0:
                    break
                
                if monthly_rate > 0:
                    interest_month = remaining * monthly_rate
                    principal_month = emi - interest_month
                else:
                    interest_month = 0
                    principal_month = emi
                
                if principal_month > remaining:
                    principal_month = remaining
                    interest_month = 0
                
                yearly_interest += interest_month
                yearly_principal += principal_month
                remaining -= principal_month
                
                if remaining <= 0:
                    break
            
            years_list.append(year)
            principal_per_year.append(yearly_principal)
            interest_per_year.append(yearly_interest)
            
            if remaining <= 0:
                break
        
        # Create bar chart
        fig = go.Figure(data=[
            go.Bar(name='Principal', x=years_list, y=principal_per_year, marker_color='rgb(55, 83, 109)'),
            go.Bar(name='Interest', x=years_list, y=interest_per_year, marker_color='rgb(26, 118, 255)')
        ])
        
        fig.update_layout(
            title="Year-wise Payment Breakdown",
            xaxis_title="Years",
            yaxis_title="Amount (₹)",
            barmode='stack',
            hovermode='x'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.warning(f"Chart generation issue: {e}")
    
    # Add a simple amortization table toggle
    with st.expander("📋 View Year-wise Payment Schedule"):
        st.write("### Year-wise Payment Schedule")
        
        # Recalculate for table
        remaining = loan_amount
        table_data = []
        
        for year in range(1, int(years) + 1):
            yearly_principal = 0
            yearly_interest = 0
            
            for month in range(12):
                if remaining <= 0:
                    break
                
                if monthly_rate > 0:
                    interest_month = remaining * monthly_rate
                    principal_month = emi - interest_month
                else:
                    interest_month = 0
                    principal_month = emi
                
                if principal_month > remaining:
                    principal_month = remaining
                    interest_month = 0
                
                yearly_interest += interest_month
                yearly_principal += principal_month
                remaining -= principal_month
                
                if remaining <= 0:
                    break
            
            table_data.append({
                "Year": year,
                "Principal Paid": f"₹{yearly_principal:,.0f}",
                "Interest Paid": f"₹{yearly_interest:,.0f}",
                "Total Paid": f"₹{yearly_principal + yearly_interest:,.0f}"
            })
            
            if remaining <= 0:
                break
        
        st.table(table_data)

def fd_calculator():
    """Fixed Deposit Calculator"""
    st.subheader("🏦 Fixed Deposit Calculator")
    st.markdown("Calculate your FD maturity amount")
    
    col1, col2 = st.columns(2)
    
    with col1:
        deposit_amount = st.number_input("Deposit Amount (₹)", min_value=1000.0, value=50000.0, step=5000.0, key="fd_amount_input")
        years = st.number_input("Tenure (Years)", min_value=1.0, max_value=10.0, value=5.0, step=1.0, key="fd_years_input")
    
    with col2:
        interest_rate = st.number_input("Interest Rate (%)", min_value=3.0, max_value=9.0, value=7.0, step=0.5, key="fd_rate_input")
        compounding = st.selectbox("Compounding Frequency", ["Yearly", "Half-Yearly", "Quarterly"], key="fd_compounding_input")
    
    # Calculate based on compounding frequency
    if compounding == "Yearly":
        n = 1
    elif compounding == "Half-Yearly":
        n = 2
    else:
        n = 4
    
    maturity_amount = deposit_amount * (1 + (interest_rate / 100) / n) ** (n * years)
    interest_earned = maturity_amount - deposit_amount
    
    # Display Results
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Deposit Amount", f"₹{deposit_amount:,.0f}")
    with col2:
        st.metric("Interest Earned", f"₹{interest_earned:,.0f}")
    with col3:
        st.metric("Maturity Amount", f"₹{maturity_amount:,.0f}")
    
    # Additional info
    st.info(f"📊 **Summary:** ₹{deposit_amount:,.0f} invested at {interest_rate}% for {int(years)} years will grow to ₹{maturity_amount:,.0f}")
    
    # Create chart
    years_list = list(range(int(years) + 1))
    values = [deposit_amount * (1 + (interest_rate / 100) / n) ** (n * y) for y in years_list]
    
    fig = go.Figure(data=go.Scatter(x=years_list, y=values, mode='lines+markers', line=dict(width=3, color='green')))
    fig.update_layout(title="Growth Over Time", xaxis_title="Years", yaxis_title="Amount (₹)")
    st.plotly_chart(fig, use_container_width=True)

def goal_planner():
    """Investment Goal Planner with visual timeline"""
    st.subheader("🎯 Investment Goal Planner")
    st.markdown("Plan how much to save to reach your financial goals")
    
    col1, col2 = st.columns(2)
    
    with col1:
        goal_amount = st.number_input("Goal Amount (₹)", min_value=10000.0, value=500000.0, step=50000.0, key="goal_amount_input")
        years = st.number_input("Time Horizon (Years)", min_value=1.0, max_value=30.0, value=5.0, step=1.0, key="goal_years_input")
    
    with col2:
        current_savings = st.number_input("Current Savings (₹)", min_value=0.0, value=50000.0, step=10000.0, key="goal_current_input")
        expected_return = st.number_input("Expected Return (%)", min_value=1.0, max_value=20.0, value=12.0, step=0.5, key="goal_return_input")
    
    # Calculate required monthly investment
    months = years * 12
    monthly_rate = expected_return / (12 * 100)
    
    if monthly_rate > 0:
        # Future value of current savings
        fv_current = current_savings * (1 + expected_return / 100) ** years
        
        # Remaining amount needed
        remaining_needed = max(0, goal_amount - fv_current)
        
        # Calculate required monthly SIP
        if remaining_needed > 0:
            required_sip = remaining_needed * monthly_rate / ((1 + monthly_rate) ** months - 1)
        else:
            required_sip = 0
            st.success("🎉 You already have enough savings to reach your goal!")
    else:
        required_sip = (goal_amount - current_savings) / months
    
    total_investment = required_sip * months
    
    # Display Results
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Required Monthly SIP", f"₹{required_sip:,.0f}")
    with col2:
        st.metric("Total You'll Invest", f"₹{total_investment:,.0f}")
    with col3:
        st.metric("Goal Achievable", f"₹{goal_amount:,.0f}")
    
    # Progress bar
    progress = min(100, (current_savings / goal_amount) * 100)
    st.markdown("### Progress Towards Goal")
    st.progress(progress / 100)
    st.write(f"Current: ₹{current_savings:,.0f} ({progress:.1f}%) | Goal: ₹{goal_amount:,.0f}")
    
    # Timeline visualization
    st.markdown("### 📈 Goal Achievement Timeline")
    years_list = list(range(int(years) + 1))
    values = []
    
    for year in years_list:
        year_months = year * 12
        if monthly_rate > 0:
            fv = current_savings * (1 + expected_return / 100) ** year
            if required_sip > 0:
                sip_fv = required_sip * ((1 + monthly_rate) ** year_months - 1) / monthly_rate * (1 + monthly_rate)
                total = fv + sip_fv
            else:
                total = fv
        else:
            total = current_savings + (required_sip * year_months)
        values.append(total)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=years_list, y=values, mode='lines+markers', 
                             name='Growth Path', line=dict(color='#FF9933', width=3)))
    fig.add_hline(y=goal_amount, line_dash="dash", line_color="green", 
                  annotation_text="Goal Amount", annotation_position="top right")
    fig.update_layout(title="Wealth Growth Over Time", xaxis_title="Years", 
                      yaxis_title="Amount (₹)")
    st.plotly_chart(fig, use_container_width=True)
    
    # Motivation message
    if required_sip > 0:
        st.info(f"💡 **Tip:** To reach ₹{goal_amount:,.0f} in {int(years)} years, save ₹{required_sip:,.0f} monthly. Start today!")
    else:
        st.success("🎉 You're on track! Your current savings will meet your goal!")

def tax_calculator():
    """Income Tax Calculator with 80C deductions"""
    st.subheader("💰 Income Tax Calculator")
    st.markdown("Calculate your tax liability with Section 80C benefits")
    
    col1, col2 = st.columns(2)
    
    with col1:
        annual_income = st.number_input("Annual Income (₹)", min_value=0.0, value=800000.0, step=50000.0, key="tax_income_input")
        age_group = st.selectbox("Age Group", ["Below 60", "60-80", "Above 80"], key="tax_age_input")
    
    with col2:
        section_80c = st.number_input("Section 80C Investments (₹)", min_value=0.0, max_value=150000.0, value=50000.0, step=10000.0, key="tax_80c_input")
        other_deductions = st.number_input("Other Deductions (₹)", min_value=0.0, value=0.0, step=10000.0, key="tax_other_input")
    
    # Calculate taxable income
    taxable_income = max(0, annual_income - section_80c - other_deductions)
    
    # Calculate tax based on new regime
    if age_group == "Below 60":
        if taxable_income <= 250000:
            tax = 0
        elif taxable_income <= 500000:
            tax = (taxable_income - 250000) * 0.05
        elif taxable_income <= 1000000:
            tax = 12500 + (taxable_income - 500000) * 0.20
        else:
            tax = 112500 + (taxable_income - 1000000) * 0.30
    elif age_group == "60-80":
        if taxable_income <= 300000:
            tax = 0
        elif taxable_income <= 500000:
            tax = (taxable_income - 300000) * 0.05
        elif taxable_income <= 1000000:
            tax = 10000 + (taxable_income - 500000) * 0.20
        else:
            tax = 110000 + (taxable_income - 1000000) * 0.30
    else:  # Above 80
        if taxable_income <= 500000:
            tax = 0
        elif taxable_income <= 1000000:
            tax = (taxable_income - 500000) * 0.20
        else:
            tax = 100000 + (taxable_income - 1000000) * 0.30
    
    # Add cess
    cess = tax * 0.04
    total_tax = tax + cess
    
    # Display Results
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Taxable Income", f"₹{taxable_income:,.0f}")
    with col2:
        st.metric("Income Tax", f"₹{tax:,.0f}")
    with col3:
        st.metric("Total Tax (with Cess)", f"₹{total_tax:,.0f}")
    
    # Tax breakdown
    st.markdown("### 📊 Tax Breakdown")
    tax_data = {
        "Category": ["Taxable Income", "Tax Paid", "Effective Rate"],
        "Amount": [f"₹{taxable_income:,.0f}", f"₹{total_tax:,.0f}", f"{(total_tax/annual_income)*100:.1f}%"]
    }
    st.table(tax_data)
    
    # Tax saving tips
    st.markdown("### 💡 Tax Saving Tips")
    if section_80c < 150000:
        remaining = 150000 - section_80c
        st.info(f"🏦 **Maximize 80C:** You can invest ₹{remaining:,.0f} more in PPF, ELSS, or LIC to save additional tax.")
    
    st.success("""
    **Popular Tax Saving Options:**
    - **PPF:** Up to ₹1.5L, 7.1% interest, tax-free returns
    - **ELSS Mutual Funds:** Lock-in 3 years, market-linked returns
    - **NPS:** Additional ₹50,000 deduction under 80CCD(1B)
    - **Health Insurance:** Deduction up to ₹25,000 under 80D
    """)

def compare_investments():
    """Compare different investment options"""
    st.subheader("📊 Investment Comparison Tool")
    st.markdown("Compare returns across different investment options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        investment_amount = st.number_input("Investment Amount (₹)", min_value=1000.0, value=100000.0, step=10000.0, key="compare_amount_input")
        years = st.number_input("Investment Period (Years)", min_value=1.0, max_value=30.0, value=10.0, step=1.0, key="compare_years_input")
    
    with col2:
        st.markdown("### Investment Options")
        fd_rate = st.number_input("FD Rate (%)", min_value=3.0, max_value=9.0, value=7.0, step=0.5, key="compare_fd_input")
        sip_rate = st.number_input("SIP/Mutual Fund Rate (%)", min_value=5.0, max_value=20.0, value=12.0, step=0.5, key="compare_sip_input")
        ppf_rate = st.number_input("PPF Rate (%)", min_value=6.0, max_value=8.0, value=7.1, step=0.1, key="compare_ppf_input")
    
    # Calculate returns
    # FD (Lumpsum)
    fd_value = investment_amount * (1 + fd_rate / 100) ** years
    
    # SIP (Monthly investment)
    months = years * 12
    monthly_rate = sip_rate / (12 * 100)
    monthly_investment = investment_amount / months
    if monthly_rate > 0:
        sip_value = monthly_investment * ((1 + monthly_rate) ** months - 1) / monthly_rate * (1 + monthly_rate)
    else:
        sip_value = investment_amount
    
    # PPF (Lumpsum)
    ppf_value = investment_amount * (1 + ppf_rate / 100) ** years
    
    # Display comparison
    st.markdown("---")
    st.markdown("### 📈 Returns Comparison")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Fixed Deposit", f"₹{fd_value:,.0f}", delta=f"+ ₹{fd_value - investment_amount:,.0f}")
        st.caption(f"@{fd_rate}% p.a.")
    
    with col2:
        st.metric("SIP / Mutual Fund", f"₹{sip_value:,.0f}", delta=f"+ ₹{sip_value - investment_amount:,.0f}")
        st.caption(f"@{sip_rate}% p.a.")
    
    with col3:
        st.metric("PPF", f"₹{ppf_value:,.0f}", delta=f"+ ₹{ppf_value - investment_amount:,.0f}")
        st.caption(f"@{ppf_rate}% p.a. (Tax Free)")
    
    # Comparison chart
    options = ['Fixed Deposit', 'SIP/Mutual Fund', 'PPF']
    values = [fd_value, sip_value, ppf_value]
    
    fig = go.Figure(data=[
        go.Bar(name='Final Value', x=options, y=values, marker_color=['#FF9933', '#138808', '#000080'])
    ])
    
    fig.update_layout(title=f"₹{investment_amount:,.0f} Investment After {int(years)} Years", 
                      yaxis_title="Amount (₹)", showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    
    # Recommendation
    st.markdown("### 🎯 Recommendation")
    best = max([(fd_value, "FD"), (sip_value, "SIP/Mutual Fund"), (ppf_value, "PPF")])
    
    if best[1] == "FD":
        st.success(f"📌 **Fixed Deposit** gives the highest returns for this investment. Good for risk-averse investors.")
    elif best[1] == "SIP/Mutual Fund":
        st.success(f"📌 **SIP/Mutual Funds** give the highest returns. Good for long-term wealth creation with moderate risk.")
    else:
        st.success(f"📌 **PPF** gives the highest returns with tax benefits. Excellent for retirement planning.")

def health_score():
    """Calculate Financial Health Score"""
    st.subheader("💪 Financial Health Score")
    st.markdown("Check how financially healthy you are")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Monthly Numbers")
        monthly_income = st.number_input("Monthly Income (₹)", min_value=0.0, value=50000.0, step=5000.0, key="health_income_input")
        monthly_savings = st.number_input("Monthly Savings (₹)", min_value=0.0, value=10000.0, step=1000.0, key="health_savings_input")
    
    with col2:
        st.markdown("### 💳 Debt & Emergency")
        monthly_emi = st.number_input("Monthly EMI (₹)", min_value=0.0, value=5000.0, step=1000.0, key="health_emi_input")
        emergency_fund = st.number_input("Emergency Fund (₹)", min_value=0.0, value=50000.0, step=10000.0, key="health_emergency_input")
    
    # Calculate ratios
    savings_rate = (monthly_savings / monthly_income) * 100 if monthly_income > 0 else 0
    debt_to_income = (monthly_emi / monthly_income) * 100 if monthly_income > 0 else 0
    emergency_months = emergency_fund / monthly_income if monthly_income > 0 else 0
    
    # Calculate score
    score = 0
    insights = []
    
    # Savings rate
    if savings_rate >= 20:
        score += 30
        insights.append("✅ **Excellent savings rate!** You're saving 20%+ of your income.")
    elif savings_rate >= 10:
        score += 20
        insights.append("👍 **Good savings rate.** Try to reach 20% for faster wealth building.")
    else:
        score += 10
        insights.append("⚠️ **Low savings rate.** Aim to save at least 10-20% of your income.")
    
    # Debt ratio
    if debt_to_income <= 20:
        score += 30
        insights.append("✅ **Healthy debt level!** Your EMIs are within 20% of income.")
    elif debt_to_income <= 40:
        score += 20
        insights.append("👍 **Moderate debt.** Keep EMIs under 30-40% of income.")
    else:
        score += 10
        insights.append("⚠️ **High debt burden.** Consider reducing loans or increasing income.")
    
    # Emergency fund
    if emergency_months >= 6:
        score += 40
        insights.append("✅ **Excellent emergency fund!** You have 6+ months of expenses saved.")
    elif emergency_months >= 3:
        score += 25
        insights.append("👍 **Good emergency fund.** Aim for 6 months of expenses.")
    else:
        score += 15
        insights.append("⚠️ **Low emergency fund.** Build 3-6 months of expenses for safety.")
    
    # Display Score
    st.markdown("---")
    st.markdown("### 🎯 Your Financial Health Score")
    
    if score >= 80:
        st.success(f"### 🌟 Excellent! Score: {score}/100")
        st.balloons()
    elif score >= 60:
        st.info(f"### 👍 Good! Score: {score}/100")
    else:
        st.warning(f"### 📈 Needs Improvement! Score: {score}/100")
    
    # Gauge chart
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text': "Financial Health Score"},
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': "#FF9933"},
            'steps': [
                {'range': [0, 40], 'color': "lightgray"},
                {'range': [40, 70], 'color': "gray"},
                {'range': [70, 100], 'color': "darkgray"}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90}}))
    
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)
    
    # Display insights
    st.markdown("### 📋 Insights & Recommendations")
    for insight in insights:
        st.write(insight)
    
    # Action plan
    st.markdown("### 🚀 Action Plan")
    if savings_rate < 20:
        st.write("• **Increase savings:** Automate transfers to savings/investment accounts")
    if debt_to_income > 30:
        st.write("• **Reduce debt:** Focus on paying high-interest loans first")
    if emergency_months < 6:
        st.write("• **Build emergency fund:** Set aside 3-6 months of expenses")
    if score >= 80:
        st.write("• **Great work!** Consider investing surplus in diversified assets")