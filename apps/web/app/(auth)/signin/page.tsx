import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { LoginButton } from './components/ui/LoginButton';

export default function SignInPage() {
  return (
    <Card className="w-full max-w-md">
      <CardHeader className="space-y-1">
        <CardTitle className="text-2xl text-center">サインイン</CardTitle>
        <CardDescription className="text-center">
          Google アカウントでログインしてください
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <LoginButton />
      </CardContent>
    </Card>
  );
}
