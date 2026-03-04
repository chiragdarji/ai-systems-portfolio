---
title: "Experiment 01 — Temperature Results"
tags: [experiment, temperature, results, gpt-4o-mini]
aliases: [temperature-results, exp-01-results]
---

# Experiment 01 — Temperature Analysis Results
> **Model**: `gpt-4o-mini`  |  **Temperatures tested**: [0.0, 0.3, 0.7, 1.0, 1.5]  |  **Runs per config**: 2
---
## Domain: `general`
**Prompt:** *Explain what an LLM is in one paragraph.*
### Temperature `0.0`
**Run 1** — 129 tokens, 3487 ms
```
A Large Language Model (LLM) is a type of artificial intelligence that uses deep learning techniques, particularly neural networks, to understand, generate, and manipulate human language. These models are trained on vast amounts of text data, allowing them to learn patterns, grammar, context, and even nuances of language. LLMs can perform a variety of language-related tasks, such as text generation, translation, summarization, and question-answering, by predicting the next word in a sequence based on the input they receive. Their size, typically measured in billions of parameters, enables them to capture complex linguistic structures and provide coherent and contextually relevant responses.
```
**Run 2** — 126 tokens, 4737 ms
```
A Large Language Model (LLM) is a type of artificial intelligence that uses deep learning techniques, particularly neural networks, to understand, generate, and manipulate human language. These models are trained on vast amounts of text data, allowing them to learn patterns, context, and nuances of language. LLMs can perform a variety of language-related tasks, such as text generation, translation, summarization, and question-answering, by predicting the next word in a sequence based on the input they receive. Their size, often measured in billions of parameters, enables them to capture complex linguistic structures and deliver coherent and contextually relevant responses.
```
**Determinism check (run 1 vs run 2):** `DIFFERS`
### Temperature `0.3`
**Run 1** — 132 tokens, 3457 ms
```
A Large Language Model (LLM) is a type of artificial intelligence that is designed to understand, generate, and manipulate human language. These models are built using deep learning techniques, particularly neural networks, and are trained on vast amounts of text data to learn patterns, grammar, context, and semantics. LLMs can perform a variety of language-related tasks, such as text completion, translation, summarization, and question-answering, by predicting the next word in a sequence based on the input they receive. Their size, typically measured in billions of parameters, allows them to capture complex language structures and nuances, making them powerful tools for natural language processing applications.
```
**Run 2** — 126 tokens, 3500 ms
```
A Large Language Model (LLM) is a type of artificial intelligence designed to understand, generate, and manipulate human language. These models are built using deep learning techniques, particularly neural networks, and are trained on vast amounts of text data to learn the statistical patterns and structures of language. LLMs can perform a variety of language-related tasks, such as text generation, translation, summarization, and question-answering, by predicting the next word in a sequence based on the context provided. Their size, typically measured in billions of parameters, allows them to capture complex linguistic nuances, making them powerful tools for natural language processing applications.
```
**Determinism check (run 1 vs run 2):** `DIFFERS`
### Temperature `0.7`
**Run 1** — 131 tokens, 4942 ms
```
A Large Language Model (LLM) is a type of artificial intelligence designed to understand, generate, and manipulate human language by leveraging vast amounts of text data during its training process. These models utilize deep learning techniques, particularly neural networks, to learn patterns, grammar, context, and meaning from the data, allowing them to perform a variety of language-related tasks such as text generation, translation, summarization, and answering questions. LLMs, exemplified by models like OpenAI's GPT series, are characterized by their large-scale architecture, encompassing millions or even billions of parameters, which enable them to produce coherent and contextually relevant responses across diverse topics.
```
**Run 2** — 124 tokens, 3804 ms
```
A Large Language Model (LLM) is an advanced artificial intelligence system designed to understand, generate, and manipulate human language. It is trained on vast amounts of text data using machine learning techniques, particularly deep learning, enabling it to recognize patterns, context, and semantics within language. LLMs can perform a variety of tasks such as text generation, translation, summarization, and question-answering, making them versatile tools in applications ranging from customer support to content creation. Their effectiveness comes from their ability to predict the next word in a sentence based on preceding words, allowing them to generate coherent and contextually relevant responses.
```
**Determinism check (run 1 vs run 2):** `DIFFERS`
### Temperature `1.0`
**Run 1** — 109 tokens, 3477 ms
```
A Large Language Model (LLM) is a type of artificial intelligence designed to understand, generate, and manipulate human language by processing vast amounts of text data. It utilizes deep learning techniques, particularly neural networks, to analyze patterns and relationships in language, enabling it to perform a wide range of tasks such as text completion, translation, summarization, and conversation. LLMs are characterized by their scale, often comprising billions of parameters, which allow them to capture nuanced meanings and contexts, making them proficient in generating coherent and contextually relevant responses.
```
**Run 2** — 122 tokens, 2795 ms
```
A Large Language Model (LLM) is a type of artificial intelligence that uses deep learning algorithms to understand, generate, and manipulate human language. These models are trained on vast amounts of text data, allowing them to learn the nuances of language, including grammar, context, and semantics. LLMs utilize transformer architectures, which enable them to process language in a more efficient and nuanced manner compared to earlier models. They are capable of performing a wide range of tasks, such as language translation, text summarization, question answering, and even creative writing, making them powerful tools for various applications in natural language processing.
```
**Determinism check (run 1 vs run 2):** `DIFFERS`
### Temperature `1.5`
**Run 1** — 136 tokens, 3015 ms
```
A large language model (LLM) is a type of artificial intelligence that employs deep learning techniques, specifically neural networks, to process and generate human-like text based on the patterns it has learned from massive datasets. Trained on diverse texts from books, articles, websites, and other written materials, LLMs can perform various language-related tasks, such as language translation, summarization, and contextually aware responding, while having the ability to understand the nuances of grammar, context, and content variation. Their effectiveness stems from the sheer scale of their architecture, these models often containing billions of parameters that enable them to capture a wide range of linguistic commonalities and subtleties.
```
**Run 2** — 118 tokens, 3339 ms
```
A Large Language Model (LLM) is a type of artificial intelligence designed to comprehend and generate human language at scale. It employs machine learning techniques, particularly deep learning, to analyze vast amounts of text data, enabling it to understand contextual relationships between words and phrases. LLMs can perform a variety of natural language processing tasks, such as translation, summarization, and conversation, demonstrating capability for nuanced coherent text generation. Due to their massive scale in terms of parameters and training data, LLMs exhibit advanced proficiency in languages and are utilized across various applications from chatbots to content creation.
```
**Determinism check (run 1 vs run 2):** `DIFFERS`
---
## Domain: `financial`
**Prompt:** *Summarise the key risk factors an investor should consider before buying a tech stock.*
### Temperature `0.0`
**Run 1** — 384 tokens, 7487 ms
```
When considering an investment in a tech stock, investors should evaluate several key risk factors:

1. **Market Volatility**: Tech stocks can be highly volatile, influenced by market trends, investor sentiment, and economic conditions. Price swings can be significant.

2. **Regulatory Risks**: The tech industry is subject to various regulations, including data privacy laws, antitrust scrutiny, and intellectual property rights. Changes in regulations can impact business operations and profitability.

3. **Competition**: The tech sector is characterized by rapid innovation and intense competition. New entrants and disruptive technologies can quickly erode market share and profitability.

4. **Technological Obsolescence**: Rapid advancements in technology can render products or services obsolete. Companies must continuously innovate to stay relevant.

5. **Dependency on Key Personnel**: Many tech companies rely heavily on a small number of key individuals. The loss of these individuals can adversely affect the company's performance.

6. **Supply Chain Risks**: Tech companies often depend on global supply chains for components. Disruptions due to geopolitical tensions, natural disasters, or pandemics can impact production and delivery.

7. **Financial Health**: Investors should assess the company's financial stability, including revenue growth, profitability, cash flow, and debt levels. High levels of debt can be particularly risky in a downturn.

8. **Market Sentiment and Speculation**: Tech stocks can be subject to speculative trading, leading to inflated valuations that may not reflect the underlying fundamentals.

9. **Cybersecurity Threats**: As technology companies handle vast amounts of data, they are prime targets for cyberattacks. A significant breach can lead to financial losses and reputational damage.

10. **Global Economic Conditions**: Economic downturns can affect consumer spending and business investment in technology, impacting revenue growth.

Investors should conduct thorough due diligence and consider these factors in the context of their investment strategy and risk tolerance.
```
**Run 2** — 376 tokens, 7630 ms
```
When considering an investment in a tech stock, investors should evaluate several key risk factors:

1. **Market Volatility**: Tech stocks can be highly volatile, influenced by market trends, investor sentiment, and economic conditions. Price swings can be significant.

2. **Regulatory Risks**: The tech industry is subject to various regulations, including data privacy laws, antitrust scrutiny, and intellectual property rights. Changes in regulations can impact business operations and profitability.

3. **Competition**: The tech sector is characterized by rapid innovation and intense competition. New entrants and disruptive technologies can quickly erode market share and profitability.

4. **Technological Obsolescence**: Rapid advancements in technology can render products or services obsolete. Companies must continuously innovate to stay relevant.

5. **Dependency on Key Personnel**: Many tech companies rely heavily on a small number of key individuals. The loss of these personnel can adversely affect the company's performance.

6. **Supply Chain Risks**: Tech companies often depend on global supply chains for components. Disruptions due to geopolitical tensions, natural disasters, or pandemics can impact production and delivery.

7. **Financial Health**: Investors should assess the company's financial stability, including cash flow, debt levels, and profitability. High levels of debt can be particularly risky in a downturn.

8. **Market Sentiment and Speculation**: Tech stocks can be subject to speculative trading, leading to inflated valuations that may not reflect the underlying fundamentals.

9. **Global Economic Conditions**: Economic downturns can affect consumer spending and business investment in technology, impacting revenue growth.

10. **Cybersecurity Risks**: As tech companies often handle sensitive data, they are vulnerable to cyberattacks, which can lead to financial losses and reputational damage.

Investors should conduct thorough due diligence and consider these factors in the context of their investment strategy and risk tolerance.
```
**Determinism check (run 1 vs run 2):** `DIFFERS`
### Temperature `0.3`
**Run 1** — 400 tokens, 7221 ms
```
When considering an investment in a tech stock, investors should evaluate several key risk factors:

1. **Market Volatility**: Tech stocks can be highly volatile, influenced by market trends, investor sentiment, and economic conditions. Sudden price swings can lead to significant losses.

2. **Regulatory Risks**: The tech industry is subject to various regulations, including data privacy laws, antitrust scrutiny, and intellectual property rights. Changes in regulations can impact a company's operations and profitability.

3. **Competition**: The tech sector is characterized by rapid innovation and intense competition. Companies may face challenges from existing competitors and new entrants, which can erode market share and margins.

4. **Technological Obsolescence**: Rapid technological advancements can render products or services obsolete. Companies must continuously innovate to stay relevant, which can require significant investment.

5. **Dependency on Key Personnel**: Many tech companies rely heavily on a small number of key individuals. The loss of these personnel can negatively impact the company’s strategic direction and operational effectiveness.

6. **Supply Chain Risks**: Tech companies often depend on complex global supply chains for components. Disruptions due to geopolitical tensions, natural disasters, or pandemics can affect production and delivery.

7. **Financial Health**: Investors should assess the company's financial stability, including revenue growth, profitability, cash flow, and debt levels. High levels of debt can increase financial risk, especially in downturns.

8. **Valuation Concerns**: Many tech stocks trade at high price-to-earnings (P/E) ratios, which can lead to overvaluation. Investors should be cautious of investing in stocks that may not justify their valuations based on fundamentals.

9. **Cybersecurity Risks**: Tech companies are often targets for cyberattacks. A significant breach can lead to financial losses, reputational damage, and regulatory penalties.

10. **Global Economic Factors**: Economic downturns, inflation, and changes in consumer spending can impact tech companies, particularly
```
**Run 2** — 366 tokens, 7968 ms
```
When considering an investment in a tech stock, investors should evaluate the following key risk factors:

1. **Market Volatility**: Tech stocks can be highly volatile, with prices subject to rapid changes based on market sentiment, news, and trends.

2. **Regulatory Risks**: The tech industry is often subject to changing regulations, including data privacy laws, antitrust scrutiny, and intellectual property issues, which can impact operations and profitability.

3. **Competition**: The tech sector is characterized by intense competition, with new entrants and disruptive technologies posing risks to established companies.

4. **Innovation and Product Lifecycle**: Rapid technological advancements can render products obsolete. Companies must continuously innovate to stay relevant, which can be costly and uncertain.

5. **Economic Sensitivity**: Tech stocks can be sensitive to economic cycles. During downturns, consumer and business spending on technology may decline, affecting revenues.

6. **Supply Chain Disruptions**: Many tech companies rely on global supply chains. Disruptions due to geopolitical tensions, natural disasters, or pandemics can impact production and delivery.

7. **Cybersecurity Risks**: As technology companies handle vast amounts of data, they are prime targets for cyberattacks, which can lead to financial losses and reputational damage.

8. **Valuation Concerns**: Many tech stocks may trade at high price-to-earnings ratios, leading to concerns about overvaluation and potential corrections.

9. **Management and Governance**: The effectiveness of a company's management team and governance practices can significantly impact its performance and strategic direction.

10. **Global Market Exposure**: Many tech companies operate internationally, exposing them to foreign market risks, currency fluctuations, and geopolitical instability.

Investors should conduct thorough due diligence and consider these factors in the context of their investment strategy and risk tolerance.
```
**Determinism check (run 1 vs run 2):** `DIFFERS`
### Temperature `0.7`
**Run 1** — 400 tokens, 7951 ms
```
When considering an investment in a tech stock, investors should evaluate the following key risk factors:

1. **Market Volatility**: Tech stocks can be highly volatile, with prices influenced by market sentiment, technological advancements, and economic conditions.

2. **Regulatory Risks**: The tech industry is subject to significant regulation, including data privacy laws, antitrust scrutiny, and changes in trade policies, which can impact operations and profitability.

3. **Competition**: The tech sector is characterized by rapid innovation and fierce competition. New entrants or advancements from competitors can quickly erode market share and profit margins.

4. **Technological Obsolescence**: Rapid technological change means that products and services can become outdated quickly. Companies must continuously innovate to stay relevant, which requires substantial investment.

5. **Dependence on Key Personnel**: Many tech companies rely heavily on a small number of key individuals for leadership and innovation. The loss of these individuals can adversely affect the company’s performance.

6. **Supply Chain Issues**: Tech firms often depend on a global supply chain for components. Disruptions, such as those caused by geopolitical tensions or pandemics, can impact production and delivery.

7. **Intellectual Property Risks**: The tech industry is reliant on patents and proprietary technology. Infringement or challenges to a company’s intellectual property can lead to costly legal battles.

8. **Financial Stability**: Investors should assess the company’s financial health, including cash flow, debt levels, and profitability, as tech companies can have high burn rates, especially startups.

9. **Market Saturation**: Some segments of the tech market may be nearing saturation, limiting growth potential for certain companies or products.

10. **Cybersecurity Threats**: Increased reliance on digital infrastructure exposes tech companies to cybersecurity risks, which can lead to financial losses and reputational damage.

11. **Global Economic Factors**: Economic downturns can lead to reduced consumer and enterprise spending on technology, impacting revenue growth and
```
**Run 2** — 400 tokens, 7774 ms
```
When considering an investment in tech stocks, investors should evaluate several key risk factors:

1. **Market Volatility**: Tech stocks can experience significant price fluctuations due to market sentiment, regulatory changes, and global economic conditions. This volatility can lead to substantial gains or losses.

2. **Competition**: The technology sector is highly competitive, with rapid advancements and new entrants. Companies may struggle to maintain market share or profitability if they fail to innovate or differentiate their products.

3. **Regulatory Risks**: Technology companies are subject to various regulations, including data privacy laws, antitrust scrutiny, and intellectual property protections. Changes in regulations can impact operations and profitability.

4. **Dependency on Innovation**: The sector relies heavily on continuous innovation. A company's inability to keep pace with technological advancements can lead to obsolescence and loss of market position.

5. **Economic Sensitivity**: Tech stocks can be sensitive to economic downturns. During recessions, consumers and businesses may cut back on technology spending, adversely affecting revenue.

6. **Supply Chain Risks**: Many tech companies depend on global supply chains for components. Disruptions (e.g., geopolitical tensions, natural disasters) can impact production and delivery timelines.

7. **Cybersecurity Threats**: As technology companies increasingly rely on digital platforms, they face heightened risks of cyberattacks. Breaches can lead to financial losses, legal liabilities, and damage to reputation.

8. **Valuation Concerns**: Many tech stocks trade at high price-to-earnings ratios, reflecting growth expectations. If a company fails to meet these expectations, its stock price could decline sharply.

9. **Talent Acquisition and Retention**: The tech sector is highly dependent on skilled labor, and competition for talent can drive up costs and impact a company's ability to innovate and execute its business strategy.

10. **Geopolitical Risks**: International trade tensions, tariffs, and geopolitical instability can affect tech companies, particularly those with global operations or supply
```
**Determinism check (run 1 vs run 2):** `DIFFERS`
### Temperature `1.0`
**Run 1** — 400 tokens, 7521 ms
```
When considering an investment in tech stocks, investors should evaluate the following key risk factors:

1. **Market Volatility**: Tech stocks are often subject to higher volatility compared to other sectors. Rapid changes in market sentiment can lead to significant price fluctuations.

2. **Competition**: The technology sector is characterized by fierce competition. Companies must continuously innovate and adapt to remain relevant. Failure to do so can result in market share loss.

3. **Regulatory Risks**: Tech companies can face various regulatory challenges, including data privacy laws, antitrust scrutiny, and changes in tax policies. Compliance costs or penalties can impact profitability.

4. **Dependency on Innovation**: The success of tech companies often hinges on their ability to develop new products and technologies. A failure to innovate can lead to stagnation and decreased market share.

5. **Economic Sensitivity**: Many tech stocks are sensitive to economic cycles. During downturns or recessions, consumers and businesses may cut back on tech spending, affecting revenues.

6. **Supply Chain Issues**: Tech companies often rely on complex supply chains for components and materials. Disruptions, such as those caused by geopolitical tensions or natural disasters, can hinder production and delivery.

7. **Intellectual Property Risks**: Protecting intellectual property is crucial in the tech sector. Companies face risks related to patent infringement and the potential for costly litigation.

8. **Cybersecurity Threats**: Tech companies are frequent targets of cyberattacks. Data breaches and security lapses can result in legal liabilities, reputational damage, and significant financial losses.

9. **Technological Obsolescence**: Rapid advancements in technology can render products obsolete. Companies must stay ahead of trends to avoid losing relevance in the marketplace.

10. **Management and Governance**: The effectiveness of a company’s leadership team and governance practices can impact its performance. Poor management or corporate governance issues can lead to strategic missteps.

By carefully analyzing these risk factors, investors can make more informed decisions
```
**Run 2** — 394 tokens, 8457 ms
```
Investors considering buying a tech stock should evaluate several key risk factors:

1. **Market Volatility**: The tech sector is often subject to rapid price fluctuations due to changes in market sentiment, economic conditions, and technological advancements.

2. **Regulatory Risks**: Technology companies may face scrutiny from governments regarding antitrust laws, data privacy regulations, and intellectual property rights, which can impact their operations and profitability.

3. **Competitive Landscape**: The tech industry is highly competitive, with constant innovation leading to potential obsolescence of products and services. New entrants or innovative competitors can disrupt established companies.

4. **Dependency on Innovation**: Tech firms rely on continuous research and development to remain competitive. Failure to innovate or bring new products to market can adversely affect a company's growth prospects.

5. **Cybersecurity Threats**: Tech companies are often targets for cyberattacks, which can lead to data breaches, loss of customer trust, and legal liabilities.

6. **Economic Sensitivity**: Economic downturns can impact consumer spending and business investment in technology, affecting sales and revenue growth.

7. **Supply Chain Risks**: Many tech companies depend on global supply chains for components and materials. Disruptions due to geopolitical events, natural disasters, or pandemics can affect production.

8. **Valuation Concerns**: Many tech stocks may be priced at high valuations relative to earnings. This can lead to increased risks if growth expectations are not met, potentially resulting in significant price corrections.

9. **Talent Acquisition and Retention**: The tech industry faces fierce competition for skilled employees. Difficulty in attracting and retaining top talent can hinder a company’s ability to innovate and grow.

10. **International Exposure**: Companies with significant international operations may face risks related to currency fluctuations, differing regulatory environments, and political instability in various markets.

Investors should thoroughly analyze these factors, along with the individual company's fundamentals, before making investment decisions in the tech sector.
```
**Determinism check (run 1 vs run 2):** `DIFFERS`
### Temperature `1.5`
**Run 1** — 362 tokens, 6933 ms
```
Investing in tech stocks can offer substantial returns, but several key risk factors must be considered:

1. **Market Volatility**: Tech stocks, particularly startups and smaller enterprises, can experience significant price fluctuations based on market sentiments, innovations, or sector shifts.

2. **Regulatory Risks**: Technologies and platforms may be subject to changing regulations and scrutiny (e.g., antitrust laws), which can impact operations, profitability, and stock prices.

3. **Innovation and Competition**: Rapid technological advancements coexist with aggressive competition; a company can potentialize exit if unable to innovate or maintain market presence against competitors.

4. **Profitability and Revenue Dependence**: Many tech companies may not be profitable, especially in growth stages. Their revenues often depend on future projections which can change due to market dynamics.

5. **Bubbles and Overvaluation**: The tech sector can have periods of speculative trading, leading to overvaluation where stock prices exceed their underlying business fundamentals.

6. **Intellectual Property Risks**: Companies are susceptible to risks involving patents and technological equivalence. Litigation or infringement could impede their competitive edge and profitability.

7. **Global Economic Factors**: Macroeconomic conditions, such as economic downturns, interest rates worldwide events, may affect tech stock performance, products' commodity costs, or supply chains. 

8. **Cybersecurity Threats**: With companies increasingly digitizing data and services, they face cybersecurity threats that could jeopardize user trust and operational stability.

9. **Talent Acquisition and Acquisition Risks**: Startups particularly face challenges in attracting / retaining top talent and may deal with changing strategies upon mergers/acquisitions by larger firms, affecting future pathways.

These risk factors can significantly impact an investment’s success, making thorough market research and analysis crucial before making investment decisions.
```
**Run 2** — 400 tokens, 7416 ms
```
Investing in tech stocks can be lucrative, but it comes with specific risks that investors should carefully evaluate before making decisions. Here are the key risk factors to consider:

1. **Market Volatility**: Tech stocks are often subject to significant price fluctuations. The sector tends to be more volatile due to changes in consumer preferences, regulatory developments, and other macroeconomic factors.

2. **Competitive Landscape**: The tech industry is highly competitive, with new entrants and incumbents constantly vying for market share. Changes in competitive dynamics can significantly impact a company’s profitability and market position.

3. **Regulatory Risks**: Tech companies often face strict regulations concerning data privacy, cybersecurity, and antitrust laws. Changes in legislation can lead to increased costs or limit operational capabilities.

4. **Technological Obsolescence**: Rapid technological advancements mean that products and services can quickly become outdated. Firms must continue innovating to avoid falling behind, which can involve substantial R&D expenditures.

5. **Dependency on Key Personnel**: Many tech companies rely heavily on a small group of skilled executives or developers. Departure of key personnel can impact operational execution and company strategy.

6. **Geopolitical Risks**: Tech companies frequently operate globally. Geopolitical tensions—including trade disputes—can disrupt supply chains, increase tariffs, or limit market access.

7. **Cybersecurity Risks**: Given the tech industry's dependence on digital infrastructure, entities are vulnerable to cyberattacks, which may lead to estate crippling, reputational harm, and liability.

8. **Growth Dependence**: Many tech companies rely on a narrative of high growth potential to drive investment. If actual returns fail to meet growth expectations, the stock could face substantial declines.

9. **Budget Constraints of Customers**: As the economic landscape changes, customers' budgetary constraints might influence their tech spend. Events like recessions could lead to reduced sales for tech companies.

10. **Value and Cash Flow Comparisons**: Some tech stocks may
```
**Determinism check (run 1 vs run 2):** `DIFFERS`
---
## Domain: `legal`
**Prompt:** *Summarise the key clauses typically found in a software licence agreement.*
### Temperature `0.0`
**Run 1** — 335 tokens, 6566 ms
```
A software license agreement typically includes the following key clauses:

1. **Grant of License**: Specifies the rights granted to the licensee, including the scope (e.g., single-user, multi-user, site license) and any limitations on use.

2. **Restrictions**: Outlines prohibited actions, such as reverse engineering, modification, distribution, or use for unlawful purposes.

3. **Term and Termination**: Defines the duration of the license and conditions under which the agreement can be terminated by either party.

4. **Payment Terms**: Details any fees associated with the license, including payment schedules, renewal fees, and penalties for late payment.

5. **Intellectual Property Rights**: Clarifies ownership of the software and any related intellectual property, affirming that the licensee does not acquire any ownership rights.

6. **Warranties and Disclaimers**: States any warranties provided by the licensor regarding the software's performance and includes disclaimers of liability for issues arising from its use.

7. **Support and Maintenance**: Describes any support services provided, including updates, bug fixes, and the duration of such services.

8. **Confidentiality**: Obligates the parties to protect any confidential information exchanged during the term of the agreement.

9. **Governing Law**: Specifies the jurisdiction and legal framework that will govern the agreement.

10. **Indemnification**: Outlines the responsibilities of each party to indemnify the other against certain claims or damages arising from the use of the software.

These clauses help define the relationship between the licensor and licensee, ensuring clarity on rights, responsibilities, and limitations.
```
**Run 2** — 322 tokens, 6472 ms
```
A software license agreement typically includes the following key clauses:

1. **Grant of License**: Specifies the rights granted to the licensee, including the scope (e.g., non-exclusive, non-transferable) and limitations on use.

2. **Restrictions**: Outlines prohibited actions, such as reverse engineering, modification, or distribution of the software.

3. **Term and Termination**: Defines the duration of the license and conditions under which the agreement can be terminated by either party.

4. **Payment Terms**: Details any fees associated with the license, including payment schedules and consequences for late payments.

5. **Intellectual Property Rights**: Clarifies ownership of the software and any related intellectual property, affirming that the licensee does not acquire any ownership rights.

6. **Warranties and Disclaimers**: States any warranties provided by the licensor regarding the software's performance and includes disclaimers of liability for issues arising from its use.

7. **Indemnification**: Specifies the obligations of one party to compensate the other for certain damages or losses, often related to third-party claims.

8. **Confidentiality**: Obligates the parties to protect any confidential information exchanged during the term of the agreement.

9. **Governing Law**: Identifies the jurisdiction and legal framework that will govern the agreement.

10. **Dispute Resolution**: Outlines the process for resolving disputes, which may include mediation or arbitration clauses.

These clauses help define the relationship between the software provider and the user, ensuring clarity on rights, responsibilities, and legal protections.
```
**Determinism check (run 1 vs run 2):** `DIFFERS`
### Temperature `0.3`
**Run 1** — 336 tokens, 6297 ms
```
A software license agreement typically includes the following key clauses:

1. **Grant of License**: Specifies the scope of the license granted to the user, including whether it is exclusive or non-exclusive, and the permitted uses of the software.

2. **Restrictions**: Outlines prohibited actions, such as copying, modifying, distributing, or reverse-engineering the software.

3. **Ownership**: Clarifies that the software and any related intellectual property rights remain the property of the licensor.

4. **Term and Termination**: Defines the duration of the license and the conditions under which the agreement can be terminated by either party.

5. **Payment Terms**: Details any fees associated with the license, including payment schedules and consequences of non-payment.

6. **Warranties and Disclaimers**: Provides any warranties regarding the software's performance and includes disclaimers of liability for issues that may arise from its use.

7. **Indemnification**: Specifies the obligations of one party to compensate the other for certain losses or damages arising from breaches of the agreement.

8. **Confidentiality**: Obligates parties to keep certain information confidential, often related to proprietary technology or business practices.

9. **Governing Law**: Identifies the jurisdiction and legal framework that will govern the agreement.

10. **Dispute Resolution**: Outlines the process for resolving disputes, which may include mediation, arbitration, or litigation.

11. **Updates and Maintenance**: Details any obligations for providing updates, support, or maintenance for the software.

These clauses collectively define the rights and responsibilities of both the licensor and licensee regarding the use of the software.
```
**Run 2** — 370 tokens, 7674 ms
```
A software license agreement typically includes the following key clauses:

1. **Grant of License**: Specifies the rights granted to the licensee, including whether the license is exclusive or non-exclusive, and the scope of use (e.g., personal, commercial).

2. **Restrictions**: Outlines prohibited actions, such as copying, modifying, distributing, or reverse-engineering the software.

3. **Term and Termination**: Defines the duration of the license and conditions under which the agreement can be terminated by either party.

4. **Fees and Payment**: Details any licensing fees, payment terms, and consequences for late payments.

5. **Intellectual Property Rights**: Clarifies ownership of the software and any related intellectual property, affirming that the licensee does not gain ownership rights.

6. **Warranties and Disclaimers**: States any warranties provided by the licensor regarding the software's performance and includes disclaimers of liability.

7. **Indemnification**: Specifies the obligations of either party to indemnify the other for claims arising from the use of the software.

8. **Support and Maintenance**: Describes any support or maintenance services provided, including response times and service levels.

9. **Confidentiality**: Obligates both parties to protect any confidential information shared during the term of the agreement.

10. **Governing Law and Jurisdiction**: Identifies the legal jurisdiction that governs the agreement and any disputes that may arise.

11. **Amendments**: Outlines the process for making changes to the agreement, typically requiring written consent from both parties.

12. **Assignment**: Specifies whether the rights and obligations under the agreement can be transferred to another party.

These clauses ensure clarity and protect the rights of both the licensor and licensee in the use of the software.
```
**Determinism check (run 1 vs run 2):** `DIFFERS`
### Temperature `0.7`
**Run 1** — 325 tokens, 7003 ms
```
A software license agreement typically includes the following key clauses:

1. **Grant of License**: Specifies the type of license granted (e.g., exclusive, non-exclusive, perpetual, or time-limited) and outlines the rights and limitations of the licensee.

2. **Scope of Use**: Defines how the software can be used, including restrictions on copying, modifying, or distributing the software.

3. **License Fees and Payment Terms**: Details any fees associated with the license, payment schedules, and consequences for non-payment.

4. **Ownership and Intellectual Property Rights**: Clarifies that the licensor retains ownership of the software and any related intellectual property rights.

5. **Support and Maintenance**: Outlines any obligations of the licensor to provide technical support, updates, or maintenance services.

6. **Warranties and Disclaimers**: States any warranties provided by the licensor regarding the software's performance and disclaimers of liability for issues arising from its use.

7. **Termination**: Specifies conditions under which the agreement may be terminated by either party, including breach of contract or insolvency.

8. **Confidentiality**: Obligates parties to maintain the confidentiality of proprietary information exchanged during the term of the agreement.

9. **Limitation of Liability**: Limits the liability of the licensor for damages arising from the use of the software.

10. **Governing Law and Dispute Resolution**: Identifies the jurisdiction and legal framework governing the agreement and outlines procedures for resolving disputes.

These clauses collectively establish the framework for the relationship between the software provider and the user.
```
**Run 2** — 391 tokens, 7590 ms
```
A software license agreement typically includes the following key clauses:

1. **Grant of License**: Specifies the rights granted to the licensee, including the type of license (e.g., exclusive, non-exclusive, perpetual, or limited), and any restrictions on use.

2. **Permitted Use**: Outlines how the software can be used, including any limitations on copying, modification, or distribution.

3. **Restrictions**: Details prohibited actions, such as reverse engineering, sharing the software with third parties, or using it for illegal purposes.

4. **Ownership and Intellectual Property Rights**: Clarifies that the licensor retains ownership of the software and all associated intellectual property rights.

5. **Maintenance and Support**: Defines any support services provided by the licensor, including updates, bug fixes, and the duration of support.

6. **Fees and Payment Terms**: Specifies the cost of the license, payment schedule, and any additional fees for support or maintenance.

7. **Term and Termination**: Outlines the duration of the license agreement and conditions under which either party may terminate the agreement.

8. **Confidentiality**: Obligates both parties to maintain the confidentiality of proprietary information exchanged during the term of the agreement.

9. **Warranties and Disclaimers**: Includes any warranties provided by the licensor regarding the software's performance, as well as disclaimers of liability for defects or issues.

10. **Limitation of Liability**: Limits the liability of the licensor in case of damages arising from the use of the software.

11. **Governing Law and Jurisdiction**: Specifies the legal jurisdiction governing the agreement and any disputes that may arise.

12. **Indemnification**: Requires one party to compensate the other for losses arising from specific claims or breaches of the agreement.

These clauses help define the legal relationship between the software provider and the user, protecting both parties' interests.
```
**Determinism check (run 1 vs run 2):** `DIFFERS`
### Temperature `1.0`
**Run 1** — 362 tokens, 7630 ms
```
A software license agreement typically includes the following key clauses:

1. **Grant of License**: Outlines the rights granted to the licensee, specifying the type of license (e.g., exclusive, non-exclusive, perpetual, or time-limited) and permitted usage (e.g., personal, commercial, number of users).

2. **Restrictions**: Details prohibitions on actions such as copying, modifying, or distributing the software, and may also prohibit reverse engineering or use in specific environments.

3. **Intellectual Property Rights**: Clarifies ownership of the software and associated intellectual property, emphasizing that the licensee does not acquire any ownership rights.

4. **Payment Terms**: Specifies any fees associated with the license, including payment schedules, renewal terms, and penalties for late payments.

5. **Support and Maintenance**: Describes any obligations for providing technical support, software updates, and maintenance, including duration and extent of services.

6. **Termination**: Defines conditions under which the license can be terminated by either party, including breaches of the agreement or non-payment.

7. **Liability and Indemnification**: Limits the liability of the licensor for damages and may include terms for indemnifying the licensor against claims arising from the licensee's use of the software.

8. **Confidentiality**: Obligates both parties to maintain the confidentiality of sensitive information exchanged during the course of the agreement.

9. **Governing Law**: Indicates which jurisdiction's laws will govern the agreement and any disputes that arise from it.

10. **Dispute Resolution**: Outlines procedures for resolving disputes, which may include arbitration or mediation requirements.

These clauses establish the legal framework for the use of the software and protect the rights of both the licensor and the licensee.
```
**Run 2** — 400 tokens, 7884 ms
```
A software license agreement typically includes the following key clauses:

1. **Grant of License**: Defines the scope of the rights granted to the licensee, including whether the license is exclusive, non-exclusive, transferable, or sublicensable.

2. **Permitted Uses**: Specifies the allowed ways the software can be used, including any restrictions on usage (e.g., personal use, commercial use, number of users).

3. **Restrictions**: Outlines limitations such as prohibition on reverse engineering, modification, distribution, or unauthorized copying of the software.

4. **Ownership and Intellectual Property**: Affirms that the licensor retains ownership rights and intellectual property related to the software.

5. **Payment and Fees**: Details any fees associated with the license, including payment terms, renewal fees, and penalties for late payments.

6. **Maintenance and Support**: Describes any maintenance or support services offered, including response times and obligations regarding updates or patches.

7. **Term and Termination**: Specifies the duration of the license and the conditions under which the agreement may be terminated by either party.

8. **Confidentiality**: Requires parties to keep proprietary information confidential and not disclose it without permission.

9. **Warranties and Disclaimers**: Sets forth any warranties provided by the licensor and includes disclaimers regarding software performance and reliability.

10. **Liability Limitations**: Limits the extent of liability for both parties, often capping damages to the amount paid for the license or excluding certain types of damages.

11. **Governing Law and Jurisdiction**: Identifies the governing law of the agreement and the jurisdiction for resolving disputes.

12. **Dispute Resolution**: Outlines the process for resolving any disputes, which may include arbitration or mediation requirements.

13. **Amendments**: Specifies how the agreement can be modified, typically requiring written consent from both parties.

These clauses collectively govern the relationship between the licensor and license
```
**Determinism check (run 1 vs run 2):** `DIFFERS`
### Temperature `1.5`
**Run 1** — 345 tokens, 6010 ms
```
Key clauses typically found in a software licence agreement include:

1. **Grant of Licence**: Specifies the rights being given to the licensee, including whether the licence is exclusive or non-exclusive, and the scope of permitted use.

2. **Restrictions**: Outlines what the licensee cannot do with the software, such as copying, modifying, or distributing it, and restrictions on the use of third-party components.

3. **Term and Termination**: Defines the duration of the licence, conditions under which it may be terminated by either party, and effects of termination on the software use.

4. **Ownership**: Clarifies that the licensor retains all rights, titles, and interests in the software, asserting properties like copyrights and patents.

5. **Payment Terms**: Details the cost of the licence, payment timeline, and any fees associated with future updates or support.

6. **Warranties and Disclaimers**: May include a warranty regarding the software’s performance and disclaimers to limit liability for issues related to its use.

7. **Indemnification**: A clause outlining whether either party will compensate the other for certain types of losses or damages.

8. **Confidentiality**: Mandates that both parties keep certain information confidential, protecting proprietary software-related information.

9. **Governing Law**: States what jurisdiction’s laws will govern the agreement and how disputes will be resolved.

10. **Limitation of Liability**: Includes provisions aimed at limiting the liability of the licensor, often specifying the maximum amount of damages that may be sought.

These clauses serve to define the performance expectations, legal responsibilities, and agreed-upon terms of use for the software in question.
```
**Run 2** — 374 tokens, 6752 ms
```
A software licence agreement typically includes the following key clauses:

1. **Grant of Licence**: Specifies the rights granted to the licensee to use the software, including limitations on use and the nature of the licence (e.g., non-exclusive, non-transferable).

2. **Restrictions**: Outlines prohibited actions, such as modifying, copying, distributing, or reverse-engineering the software, and any usage restrictions.

3. **Ownership and Intellectual Property**: Confirms that the licensor retains ownership of the software and any related intellectual property rights.

4. **Term and Termination**: Specifies the duration of the licence and the conditions under which the agreement can be terminated by either party, such as breach of terms.

5. **Payment and Fees**: Details the financial terms, including any upfront fees, subscription costs, royalties, or ongoing maintenance fees, if applicable.

6. **Maintenance and Support**: Describes the terms of any included support or maintenance services provided by the licensor, thresholds for uptime, updates, or upgrades.

7. **Warranties and Disclaimers**: Clarifies any warranties regarding the software’s performance, and disclaims certain liabilities, potentially limiting the licensor's liability for indirect, consequential, or incidental damages.

8. **Confidentiality**: Establishes the obligations of both parties to protect confidential information shared during the agreement.

9. **Indemnification**: Outlines the responsibilities regarding defending against claims likely rises from the software's utilization or lapses therein.

10. **Governing Law and Jurisdiction**: Specifies the legal framework governing the agreement and outlines the jurisdiction for resolving disputes.

11. **Change and Amendment**: Describes the process through which the agreement may be modified.

This summary highlights the standard elements, though actual licence agreements may vary based on individual circumstances and requirements.
```
**Determinism check (run 1 vs run 2):** `DIFFERS`
---
## Domain: `code`
**Prompt:** *Write a Python function that calculates compound interest given principal, rate, time, and n.*
### Temperature `0.0`
**Run 1** — 270 tokens, 4628 ms
```
Here is a Python function that calculates compound interest given the principal amount, annual interest rate, time in years, and the number of times that interest is compounded per year:

```python
def calculate_compound_interest(principal, rate, time, n):
    """
    Calculate compound interest.

    :param principal: The initial amount of money (the principal)
    :param rate: The annual interest rate (in decimal)
    :param time: The time the money is invested or borrowed for (in years)
    :param n: The number of times that interest is compounded per year
    :return: The amount of money accumulated after n years, including interest.
    """
    amount = principal * (1 + rate / n) ** (n * time)
    return amount

# Example usage:
principal = 1000  # Principal amount
rate = 0.05      # Annual interest rate (5%)
time = 10        # Time in years
n = 4            # Compounded quarterly

total_amount = calculate_compound_interest(principal, rate, time, n)
print(f"Total amount after {time} years: ${total_amount:.2f}")
```

This function will return the total amount after the specified time, including the compound interest. You can adjust the parameters to test different scenarios.
```
**Run 2** — 270 tokens, 4362 ms
```
Here is a Python function that calculates compound interest given the principal amount, annual interest rate, time in years, and the number of times that interest is compounded per year:

```python
def calculate_compound_interest(principal, rate, time, n):
    """
    Calculate compound interest.

    :param principal: The initial amount of money (the principal)
    :param rate: The annual interest rate (in decimal)
    :param time: The time the money is invested or borrowed for (in years)
    :param n: The number of times that interest is compounded per year
    :return: The amount of money accumulated after n years, including interest.
    """
    amount = principal * (1 + rate / n) ** (n * time)
    return amount

# Example usage:
principal = 1000  # Principal amount
rate = 0.05      # Annual interest rate (5%)
time = 10        # Time in years
n = 4            # Compounded quarterly

total_amount = calculate_compound_interest(principal, rate, time, n)
print(f"Total amount after {time} years: ${total_amount:.2f}")
```

This function computes the total amount after the specified time period, including the compound interest. You can adjust the parameters to test different scenarios.
```
**Determinism check (run 1 vs run 2):** `DIFFERS`
### Temperature `0.3`
**Run 1** — 239 tokens, 4728 ms
```
Here is a Python function that calculates compound interest given the principal amount, annual interest rate, time in years, and the number of times that interest is compounded per year:

```python
def compound_interest(principal, rate, time, n):
    """
    Calculate compound interest.

    Parameters:
    principal (float): The initial amount of money.
    rate (float): The annual interest rate (in decimal).
    time (float): The time the money is invested or borrowed for (in years).
    n (int): The number of times that interest is compounded per year.

    Returns:
    float: The amount of money accumulated after n years, including interest.
    """
    amount = principal * (1 + rate / n) ** (n * time)
    return amount

# Example usage:
# principal = 1000
# rate = 0.05  # 5%
# time = 10    # 10 years
# n = 12      # compounded monthly
# total_amount = compound_interest(principal, rate, time, n)
# print(total_amount)
```

You can uncomment the example usage to test the function with specific values.
```
**Run 2** — 276 tokens, 5522 ms
```
Here is a Python function that calculates compound interest given the principal amount, annual interest rate, time in years, and the number of times that interest is compounded per year:

```python
def calculate_compound_interest(principal, rate, time, n):
    """
    Calculate compound interest.

    :param principal: The initial amount of money (the principal).
    :param rate: The annual interest rate (as a decimal).
    :param time: The time the money is invested or borrowed for, in years.
    :param n: The number of times that interest is compounded per year.
    :return: The amount of money accumulated after n years, including interest.
    """
    amount = principal * (1 + rate / n) ** (n * time)
    return amount

# Example usage:
principal = 1000  # Principal amount
rate = 0.05      # Annual interest rate (5%)
time = 10        # Time in years
n = 4            # Compounded quarterly

total_amount = calculate_compound_interest(principal, rate, time, n)
print(f"Total amount after {time} years: ${total_amount:.2f}")
```

This function will return the total amount after the specified time, including the compound interest. You can adjust the parameters in the example usage to test with different values.
```
**Determinism check (run 1 vs run 2):** `DIFFERS`
### Temperature `0.7`
**Run 1** — 270 tokens, 4526 ms
```
Here's a Python function that calculates compound interest given the principal amount, annual interest rate, time (in years), and the number of times that interest is compounded per year.

```python
def compound_interest(principal, rate, time, n):
    """
    Calculate the compound interest.

    Parameters:
    principal (float): the initial amount of money
    rate (float): the annual interest rate (as a decimal)
    time (float): the time the money is invested or borrowed for, in years
    n (int): the number of times that interest is compounded per year

    Returns:
    float: the amount of money accumulated after n years, including interest
    """
    amount = principal * (1 + rate / n) ** (n * time)
    return amount

# Example usage:
principal = 1000  # Principal amount
rate = 0.05      # Annual interest rate (5%)
time = 10        # Time in years
n = 12           # Compounded monthly

total_amount = compound_interest(principal, rate, time, n)
print(f"The total amount after {time} years is: ${total_amount:.2f}")
```

This function calculates the total amount after applying compound interest and returns it. You can adjust the parameters as needed to test different scenarios.
```
**Run 2** — 313 tokens, 5475 ms
```
Certainly! Below is a Python function that calculates compound interest based on the principal amount, annual interest rate, time (in years), and the number of times that interest is compounded per year.

```python
def calculate_compound_interest(principal, rate, time, n):
    """
    Calculate the compound interest.
    
    :param principal: The initial amount of money (the principal).
    :param rate: The annual interest rate (in decimal).
    :param time: The time the money is invested or borrowed for, in years.
    :param n: The number of times that interest is compounded per year.
    :return: The amount of money accumulated after n years, including interest.
    """
    amount = principal * (1 + rate / n) ** (n * time)
    return amount

# Example usage
if __name__ == "__main__":
    principal_amount = 1000  # Principal amount
    annual_rate = 0.05       # 5% interest rate
    time_years = 10          # Time in years
    compoundings_per_year = 4 # Quarterly compounding

    final_amount = calculate_compound_interest(principal_amount, annual_rate, time_years, compoundings_per_year)
    print(f"The total amount after {time_years} years is: ${final_amount:.2f}")
```

You can adjust the values of `principal_amount`, `annual_rate`, `time_years`, and `compoundings_per_year` to calculate compound interest for different scenarios.
```
**Determinism check (run 1 vs run 2):** `DIFFERS`
### Temperature `1.0`
**Run 1** — 284 tokens, 4676 ms
```
Here's a Python function that calculates compound interest based on the principal amount, annual interest rate, time in years, and the number of times that interest is compounded per year (n):

```python
def compound_interest(principal, rate, time, n):
    """
    Calculate compound interest.

    Parameters:
    principal (float): The initial amount of money (the principal).
    rate (float): The annual interest rate (as a decimal).
    time (float): The time the money is invested or borrowed for (in years).
    n (int): The number of times that interest is compounded per year.

    Returns:
    float: The amount of money accumulated after interest.
    """
    amount = principal * (1 + rate / n) ** (n * time)
    return amount

# Example usage:
if __name__ == "__main__":
    principal = 1000  # Initial principal balance
    rate = 0.05      # Annual interest rate (5%)
    time = 10        # Time in years
    n = 4            # Compounded quarterly

    total_amount = compound_interest(principal, rate, time, n)
    print(f"The total amount after {time} years is: ${total_amount:.2f}")
```

This code defines the `compound_interest` function, which calculates the accumulated amount after applying compound interest and then demonstrates its usage.
```
**Run 2** — 269 tokens, 4960 ms
```
Here's a Python function that calculates compound interest given the principal, rate, time, and the number of times that interest is compounded per year:

```python
def compound_interest(principal, rate, time, n):
    """
    Calculate compound interest.

    Parameters:
    principal (float): The initial amount of money.
    rate (float): The annual interest rate (in decimal).
    time (float): The time the money is invested or borrowed for, in years.
    n (int): The number of times that interest is compounded per year.

    Returns:
    float: The amount of money accumulated after n years, including interest.
    """
    amount = principal * (1 + rate / n) ** (n * time)
    return amount

# Example usage:
principal = 1000  # initial amount
rate = 0.05      # 5% annual interest rate
time = 10        # investment duration in years
n = 12           # interest compounded monthly

total_amount = compound_interest(principal, rate, time, n)
print(f"Total amount after {time} years: ${total_amount:.2f}")
```

This function will calculate the total amount after interest has been applied, based on the provided inputs. Adjust the example usage values as needed to test with different parameters.
```
**Determinism check (run 1 vs run 2):** `DIFFERS`
### Temperature `1.5`
**Run 1** — 275 tokens, 4842 ms
```
Here's a Python function that calculates compound interest based on the provided principal, rate, time, and the number of times that interest is compounded per year (n):

```python
def compound_interest(principal, rate, time, n):
    """
    Calculate the compound interest
    
    :param principal: Initial amount of money (the principal)
    :param rate: Annual interest rate (as a decimal, e.g., 5% should be 0.05)
    :param time: Time the money is invested or borrowed for (in years)
    :param n: Number of times interest is compounded per unit year
    :return: Total amount after interest
    """
    amount = principal * (1 + rate / n) ** (n * time)
    return amount

# Example usage
principal = 1000  # Initial principal amount
rate = 0.05      # Annual interest rate (5%)
time = 10        # Time in years
n = 4            # Compounded quarterly

total_amount = compound_interest(principal, rate, time, n)
print(f"Total amount after {time} years: ${total_amount:.2f}")
```

You can customize the `principal`, `rate`, `time`, and `n` values before running the code to see how it calculates compound interest for different scenarios.
```
**Run 2** — 192 tokens, 3710 ms
```
```python
def calculate_compound_interest(principal, rate, time, n):
    """
    Calculate the compound interest.

    :param principal: Initial amount of money (the principal).
    :param rate: The annual interest rate (as a decimal).
    :param time: The number of years the money is invested or borrowed.
    :param n: The number of times that interest is compounded per year.
    :return: The amount of money accumulated after n years, including interest.
    """
    amount = principal * (1 + rate / n) ** (n * time)
    return amount

# Example usage:
# principal = 1000
# rate = 0.05  # 5%
# time = 10    # 10 years
# n = 4       # Quarterly compounding
# total_amount = calculate_compound_interest(principal, rate, time, n)
# print(total_amount)
```
```
**Determinism check (run 1 vs run 2):** `DIFFERS`
---
## Summary Stats
| Domain | Temp | Avg Tokens | Avg Latency (ms) |
|--------|------|------------|------------------|
| general | 0.0 | 128 | 4112 |
| general | 0.3 | 129 | 3478 |
| general | 0.7 | 128 | 4373 |
| general | 1.0 | 116 | 3136 |
| general | 1.5 | 127 | 3177 |
| financial | 0.0 | 380 | 7559 |
| financial | 0.3 | 383 | 7595 |
| financial | 0.7 | 400 | 7863 |
| financial | 1.0 | 397 | 7989 |
| financial | 1.5 | 381 | 7174 |
| legal | 0.0 | 328 | 6519 |
| legal | 0.3 | 353 | 6985 |
| legal | 0.7 | 358 | 7297 |
| legal | 1.0 | 381 | 7757 |
| legal | 1.5 | 360 | 6381 |
| code | 0.0 | 270 | 4495 |
| code | 0.3 | 258 | 5125 |
| code | 0.7 | 292 | 5000 |
| code | 1.0 | 276 | 4818 |
| code | 1.5 | 234 | 4276 |
