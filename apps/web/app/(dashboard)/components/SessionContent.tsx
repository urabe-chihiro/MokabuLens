"use client"

import React from "react"
import Image from "next/image"
import { useSession } from "next-auth/react"
import { Button } from "@/components/ui/button"
import { signOutUser } from "@/services/auth.service"


export function SessionContent() {
  const { data: session, status } = useSession()

  if (status === "unauthenticated") {
    return null
  }

  return (
    <div className="flex items-center space-x-4">
      {session?.user && (
        <>
        <div className="flex items-center space-x-2">
          {session.user.image && (
            <Image
              src={session.user.image}
              alt={session.user.name || "ユーザー"}
              width={32}
              height={32}
              className="w-8 h-8 rounded-full"
            />
          )}
          <span className="text-sm font-medium text-gray-700">
            {session.user.name || session.user.email}
          </span>
        </div>
        <Button
          variant="outline"
          onClick={() => signOutUser('/signin')}
        >
          ログアウト
        </Button>
        </>
      )}     
    </div>
  )
}