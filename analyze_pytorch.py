#%%
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

df = pd.read_csv('paywall_data.csv')
df['group_num'] = df['group'].apply(lambda x: 1 if x == 'treatment(Hard Paywall)' else 0)

X = df[['group_num', 'hesitation_time', 'past_sessions']].values
con_y = df['converted'].values.reshape(-1,1)
ret_y = (1-df['retained']).values.reshape(-1,1)

con_X_train, con_X_test, con_y_train, con_y_test = train_test_split(X, con_y, test_size=0.2, random_state=42)
ret_X_train, ret_X_test, ret_y_train, ret_y_test = train_test_split(X, ret_y, test_size=0.2, random_state=42)

scaler = StandardScaler()
con_X_train = scaler.fit_transform(con_X_train)
con_X_test = scaler.transform(con_X_test)

con_X_train_t = torch.FloatTensor(con_X_train)
con_y_train_t = torch.FloatTensor(con_y_train)
con_X_test_t = torch.FloatTensor(con_X_test)
con_y_test_t = torch.FloatTensor(con_y_test)

class convertPredictor(nn.Module):
    def __init__(self, input_dim):
        super(convertPredictor, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 16),
            nn.ReLU(),
            nn.Dropout(0.2), 
            nn.Linear(16, 8),
            nn.ReLU(),
            nn.Linear(8, 1),
            nn.Sigmoid() 
        )
    
    def forward(self, x):
        return self.net(x)


model = convertPredictor(con_X_train_t.shape[1])
criterion = nn.BCELoss() 
optimizer = optim.Adam(model.parameters(), lr=0.01)

print("Starting training PyTorch conversion prediction model...")
for epoch in range(100):
    model.train()
    optimizer.zero_grad()
    outputs = model(con_X_train_t)
    loss = criterion(outputs, con_y_train_t)
    loss.backward()
    optimizer.step()
    
    if (epoch + 1) % 20 == 0:
        print(f"Epoch [{epoch+1}/100], Loss: {loss.item():.4f}")


model.eval()
with torch.no_grad():
    y_pred = model(con_X_test_t)
    y_pred_cls = y_pred.round()
    accuracy = (y_pred_cls == con_y_test_t).float().mean()
    print(f"\nModel training complete! Test set accuracy: {accuracy:.2%}")


ret_X_train = scaler.fit_transform(ret_X_train)
ret_X_test = scaler.transform(ret_X_test)

ret_X_train_t = torch.FloatTensor(ret_X_train)
ret_y_train_t = torch.FloatTensor(ret_y_train)
ret_X_test_t = torch.FloatTensor(ret_X_test)
ret_y_test_t = torch.FloatTensor(ret_y_test)

class retentionPredictor(nn.Module):
    def __init__(self, input_dim):
        super(retentionPredictor, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Dropout(0.15), 
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
            nn.Sigmoid() 
        )
    
    def forward(self, x):
        return self.net(x)


ret_model = retentionPredictor(ret_X_train_t.shape[1])
ret_criterion = nn.BCELoss() 
ret_optimizer = optim.Adam(ret_model.parameters(), lr=0.001)

scheduler = optim.lr_scheduler.ReduceLROnPlateau(ret_optimizer, 'min', patience=10)

print("Starting training PyTorch retention prediction model...")
for epoch in range(300):
    ret_model.train()
    ret_optimizer.zero_grad()
    outputs = ret_model(ret_X_train_t)
    loss = ret_criterion(outputs, ret_y_train_t)
    loss.backward()
    ret_optimizer.step()
    
    if (epoch + 1) % 20 == 0:
        print(f"Epoch [{epoch+1}/100], Loss: {loss.item():.4f}")

ret_model.eval()

with torch.no_grad():
    y_pred = ret_model(ret_X_test_t)
    y_pred_cls = y_pred.round()
    ret_accuracy = (y_pred_cls == ret_y_test_t).float().mean()
    print(f"\nModel training complete! Test set accuracy: {ret_accuracy:.2%}")

# Save the model insights for the AI Agent
with open("ml_insights.txt", "w") as f:
    f.write(f"ML Conversion Prediction Accuracy: {accuracy:.2%}\n")
    f.write(f"ML Retention Prediction Accuracy: {ret_accuracy:.2%}\n")
    
# %%
