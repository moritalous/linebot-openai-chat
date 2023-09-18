# linebot-openai-chat

OpenAIとチャットができるLineボットを作成します。

## 手順

1. LINE Messaging APIの設定
  1. [LINE Developers](https://developers.line.biz/)アカウントを作成します。
  1. [こちら](https://developers.line.biz/ja/docs/messaging-api/getting-started/)を参考にチャンネルを作成します。
  1. チャンネルシークレットと[長期のチャネルアクセストークン](https://developers.line.biz/ja/docs/basics/channel-access-token/#long-lived-channel-access-token)を取得します。

1. OpenAI APIの設定
  １．OpenAIのAPIキーを発行します。

1. ビルドします。
    ```shell
    sam build
    ```

1. SAMをデプロイします。
    ```shell
    sam deploy --guided
    ```
    ```
    Stack Name [sam-app]: linebot-openai-chat
    AWS Region [ap-northeast-1]: 
    Parameter LineChannelAccessToken []: <-- 長期のチャネルアクセストークン
    Parameter LineChannelSecret []: <-- チャンネルシークレット
    Parameter NumOfHistory [10]: 
    Parameter OpenAiApiKey []: <-- OpenAI APIキー
    Parameter OpenAiModelName [gpt-3.5-turbo]: 
    #Shows you resources changes to be deployed and require a 'Y' to initiate deploy
    Confirm changes before deploy [y/N]: 
    #SAM needs permission to be able to create roles to connect to the resources in your template
    Allow SAM CLI IAM role creation [Y/n]: 
    #Preserves the state of previously provisioned resources when an operation fails
    Disable rollback [y/N]: 
    LineBotFunction Function Url has no authentication. Is this okay? [y/N]: Y
    Save arguments to configuration file [Y/n]: 
    SAM configuration file [samconfig.toml]: 
    SAM configuration environment [default]: 
    ```

    パラメーターは以下の値をセットします。

    | パラメーター | 設定値 |
    | --- | --- |
    | LineChannelAccessToken | 長期のチャネルアクセストークン |
    | LineChannelSecret | チャンネルシークレット | 
    | NumOfHistory | チャット履歴の件数（デフォルト：10） |
    | OpenAiApiKey | OpenAI APIキー |
    | OpenAiModelName | OpenAI モデル名（デフォルト：gpt-3.5-turbo） |

1. Lambdaの関数URLのURLをWebhook URLとしてLINE Messaging APIに設定し、`Use webhook`をオンにします。
1. その他、`LINE Official Account features`の設定の`Auto-reply messages`や`Greeting messages`を必要に応じて変更します。
