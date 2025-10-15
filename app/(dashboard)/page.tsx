import { Button } from "@/app/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/app/components/ui/card";

export default function Dashboard() {
  return (
    <div className="container mx-auto p-8 space-y-8">
      <div className="text-center space-y-4">
        <h1 className="text-4xl font-bold">🐾 Mokabu Lens</h1>
        <p className="text-muted-foreground">
        See the market through your own lens.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Button コンポーネント</CardTitle>
            <CardDescription>
              様々なバリエーションのボタンコンポーネント
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex flex-wrap gap-2">
              <Button>Default</Button>
              <Button variant="secondary">Secondary</Button>
              <Button variant="destructive">Destructive</Button>
              <Button variant="outline">Outline</Button>
              <Button variant="ghost">Ghost</Button>
              <Button variant="link">Link</Button>
            </div>
            <div className="flex flex-wrap gap-2">
              <Button size="sm">Small</Button>
              <Button size="default">Default</Button>
              <Button size="lg">Large</Button>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Card コンポーネント</CardTitle>
            <CardDescription>
              このカード自体もshadcn/uiのCardコンポーネントです
            </CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">
              shadcn/uiは再利用可能で美しいコンポーネントライブラリです。
              Tailwind CSSとRadix UIをベースに構築されています。
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>設定完了</CardTitle>
            <CardDescription>
              shadcn/uiのセットアップが完了しました
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                <span className="text-sm">Tailwind CSS</span>
              </div>
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                <span className="text-sm">shadcn/ui</span>
              </div>
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                <span className="text-sm">TypeScript</span>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}